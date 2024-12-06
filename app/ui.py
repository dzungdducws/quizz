import torch
import streamlit as st
from app.modules.tokenizer import load_tokenizer
from app.modules.model import load_model

# Load model and tokenizer
@st.cache_resource  # Cache the model and tokenizer to avoid reloading
def load_translation_components(model_checkpoint):
    model = load_model(model_checkpoint)
    tokenizer = load_tokenizer(model_checkpoint)
    return model, tokenizer

model_checkpoint = 'vietnqw/mbart-large-50-many-to-many-mmt-finetuned-mt'
model, tokenizer = load_translation_components(model_checkpoint)

def translate_text(input_text, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = tgt_lang

    input_tokenized = tokenizer(input_text, add_special_tokens=True, return_tensors="pt")
    input_ids = input_tokenized['input_ids'].to(model.device)
    attention_mask = input_tokenized['attention_mask'].to(model.device)

    # Generate outputs
    output_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=256
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Streamlit UI
st.title("Translation App: Mong ↔ Vietnamese")
st.write("Translate text between Mong and Vietnamese using a fine-tuned mBART model.")

# Drop-down for translation direction
direction = st.selectbox(
    "Choose translation direction",
    options=["Mong → Vietnamese", "Vietnamese → Mong"]
)

# Set source and target languages based on user selection
src_lang = "hmn_VN" if direction == "Mong → Vietnamese" else "vi_VN"
tgt_lang = "vi_VN" if direction == "Mong → Vietnamese" else "hmn_VN"

# Text input for the user
input_text = st.text_area("Enter text to translate:", value="", height=100)

# Add a button to trigger translation
if st.button("Translate"):
    if input_text.strip():
        translated_text = translate_text(input_text.strip(), src_lang, tgt_lang)
        st.text_area("Translated text:", value=translated_text, height=100, disabled=True)
    else:
        st.warning("Please enter some text to translate!")
