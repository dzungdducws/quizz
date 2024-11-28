from app.modules.tokenizer import load_tokenizer, save_tokenizer
from app.modules.model import load_model, save_model
from app.modules.text_dataloader import DataLoader
from app.utils import get_env

from transformers import (
    MBart50TokenizerFast, 
    MBartForConditionalGeneration,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)
from transformers import logging
from evaluate import load
import numpy as np

import torch
import time
import os

logging.set_verbosity_error()


def train_tokenizer(
    old_tokenizer: MBart50TokenizerFast, dataloader: DataLoader, vocab_size: int
) -> MBart50TokenizerFast:
    """
    Train a new tokenizer on a given dataset and add the new tokens to the original tokenizer to expand the vocabulary.
    """
    print(f"Training new tokenizer from {old_tokenizer.name_or_path}...")

    start = time.time()
    new_tokenizer = old_tokenizer.train_new_from_iterator(
        text_iterator=dataloader, vocab_size=vocab_size
    )
    end = time.time()
    print(f"Total training time: {end-start} seconds")

    new_tokens_set = set(new_tokenizer.get_vocab().keys())
    old_tokens_set = set(old_tokenizer.get_vocab().keys())
    tokens_to_add = list(new_tokens_set - old_tokens_set)

    combined_tokenizer = load_tokenizer(old_tokenizer.name_or_path)
    combined_tokenizer.add_tokens(tokens_to_add)

    combined_tokenizer.add_special_tokens({'additional_special_tokens': ['hmn_VN']})
    combined_tokenizer.lang_code_to_id['hmn_VN'] = combined_tokenizer('hmn_VN', add_special_tokens=False)['input_ids'][0]

    return combined_tokenizer

def expand_tokenizer(
    train_dir: str = get_env("DATA_DIR"),
    tokenizer_name: str = "facebook/mbart-large-50-many-to-many-mmt",
    model_name: str = None,
    output_tokenizer_name: str = "hmong_vietnamese_mt_mbart",
    output_model_name: str = None,
    vocab_size: int = 10000,
    batch_size: int = 1000,
    force_retrain: bool = False,
):
    try:
        if model_name is None:
            model_name = tokenizer_name
        if output_model_name is None:
            output_model_name = output_tokenizer_name

        if not force_retrain:
            trained_tokenizer_path = os.path.join(get_env('AI_MODEL_DIR'), f"tokenizer_{output_model_name}")
            trained_model_path = os.path.join(get_env('AI_MODEL_DIR'), f"model_{output_model_name}")
            if os.path.exists(trained_tokenizer_path) and os.path.exists(trained_model_path):
                tokenizer = load_tokenizer(model_name=trained_tokenizer_path)
                model = load_model(model_name=trained_model_path)
                return tokenizer, model

        model = load_model(model_name=model_name)
        tokenizer = load_tokenizer(model_name=tokenizer_name)
        dataloader = DataLoader(data_path=train_dir, batch_size=batch_size, columns=["mong"])
    except Exception:
        print('Failed to load model, tokenizer, or dataloader.')
        return

    # Expand the tokenizer vocabulary
    new_tokenizer = train_tokenizer(
        old_tokenizer=tokenizer,
        dataloader=dataloader,
        vocab_size=vocab_size,
    )
    model.resize_token_embeddings(len(new_tokenizer))

    # save model and tokenizer
    save_model(model, model_name=output_model_name)
    save_tokenizer(tokenizer=new_tokenizer, model_name=output_model_name)

    return new_tokenizer, model

def preprocess_function(tokenizer, examples, max_length=128):
    tokenizer.src_lang = 'hmn_VN';  from_lang = 'mong'
    tokenizer.tgt_lang = 'vi_VN';   to_lang = 'vietnamese'

    model_inputs_1 = tokenizer(
        text=examples[from_lang],
        text_target=examples[to_lang],
        max_length=max_length, truncation=True)
    
    tokenizer.src_lang = 'vi_VN';   from_lang = 'vietnamese'
    tokenizer.tgt_lang = 'hmn_VN';  to_lang = 'mong'

    model_inputs_2 = tokenizer(
        text=examples[from_lang],
        text_target=examples[to_lang],
        max_length=max_length, truncation=True)
    
    # combine inputs
    model_inputs = {}
    for key in model_inputs_1.keys():
        model_inputs[key] = model_inputs_1[key] + model_inputs_2[key]

    return model_inputs

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

def compute_metrics(eval_preds, metric, tokenizer):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result

def fine_tune_model(tokenizer, model, data_path=get_env('DATA_DIR'), max_length=128, batch_size=32, push_to_hub=True):
    dataloader = DataLoader(data_path=data_path, batch_size=8, test_size=0.1)
    dataloader.dataset = dataloader.dataset.map(lambda x: preprocess_function(tokenizer, x, max_length=max_length), batched=True, remove_columns=dataloader.dataset['train'].column_names)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    metric = load("sacrebleu")

    print('No. of training samples:', len(dataloader.dataset["train"]))
    model_path = os.path.join(get_env('AI_MODEL_DIR'), "mbart-large-50-M2M-mt-Mong-Viet")
    if push_to_hub:
        model_path = f"{get_env('AI_MODEL_HUB_USER')}/mbart-large-50-M2M--mt-Mong-Viet"
        print(f"Model will be pushed to hub: {model_path}")
    args = Seq2SeqTrainingArguments(
        model_path,
        evaluation_strategy = "epoch",
        learning_rate=1e-4,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        logging_strategy="epoch",
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=1,
        predict_with_generate=True,
        fp16=True,
        push_to_hub=True,
    )

    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=dataloader.dataset["train"],
        eval_dataset=dataloader.dataset["test"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=lambda x: compute_metrics(x, metric, tokenizer),
    )

    trainer.train()


def main():
    tokenizer, model = expand_tokenizer(force_retrain=True)
    fine_tune_model(tokenizer, model)

if __name__ == "__main__":
    main()
