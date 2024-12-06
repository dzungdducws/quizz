import torch
from app.modules.tokenizer import load_tokenizer
from app.modules.model import load_model


def main():
    # Load model and tokenizer
    model_checkpoint = 'vietnqw/mbart-large-50-many-to-many-mmt-finetuned-mt'
    model = load_model(model_checkpoint)
    tokenizer = load_tokenizer(model_checkpoint)
    tokenizer.src_lang = "vi_VN"
    tokenizer.tgt_lang = "hmn_VN"

    print("Translate Mong to Vietnamese")
    while True:
        text = input("Enter text: ")
        # if text.strip() == '':
        #     break

        input_tokenized = tokenizer(text, add_special_tokens=True)
        print(input_tokenized)
        input_ids = torch.tensor(input_tokenized['input_ids']).unsqueeze(0).to('cuda')
        attention_mask = torch.tensor(input_tokenized['attention_mask']).unsqueeze(0).to('cuda')

        # Generate outputs
        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=256
        )

        outputs = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]
        print(outputs)

if __name__ == "__main__":
    main()