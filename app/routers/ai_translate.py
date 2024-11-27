from fastapi import APIRouter
from ..schemas import InputTranslate, OutputTranslate
from transformers import pipeline
import torch
from app.modules.tokenizer import load_tokenizer
from app.modules.model import load_model


router = APIRouter()
# model_checkpoint = 'vietnqw/mbart-large-50-many-to-many-mmt-finetuned-mt'
# model = load_model(model_checkpoint)
# tokenizer = load_tokenizer('AI_models/tokenizer_hmong_vietnamese_mt_mbart')


@router.post("/translate", response_model=OutputTranslate)
def translate(input: InputTranslate):
    """
    Translate text from source language to target language

    Args:
        - text (str): The text to be translated
        - source_lang (str): The source language ("mong" or "viet")
        - target_lang (str): The target language ("mong" or "viet")
    """
    return {"text": do_translation(input.text, input.source_lang, input.target_lang)}


def do_translation(input_text, source_lang, target_lang):
    lang_mp = {"mong": "hmn_VN", "viet": "vi_VN"}
    tokenizer.src_lang = lang_mp[source_lang]
    tokenizer.tgt_lang = lang_mp[target_lang]

    input_tokenized = tokenizer(input_text, add_special_tokens=True)
    input_ids = torch.tensor(input_tokenized['input_ids']).unsqueeze(0).to(model.device)
    attention_mask = torch.tensor(input_tokenized['attention_mask']).unsqueeze(0).to(model.device)

    # Generate outputs
    output_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=256
    )

    # outputs = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]
    outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    return outputs[0]