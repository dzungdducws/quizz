from ..utils import get_env
from transformers import MBart50TokenizerFast
import os


def load_tokenizer(model_name: str = "facebook/mbart-large-50-many-to-many-mmt") -> MBart50TokenizerFast:
    """
    Load a tokenizer from the Hugging Face model hub
    """
    try:
        tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading tokenizer: {e}")
        raise e

    return tokenizer


def save_tokenizer(tokenizer: MBart50TokenizerFast, model_name: str) -> str:
    """
    Save a tokenizer to the output directory
    """

    model_dir = f"tokenizer_{model_name}"
    save_dir = os.path.join(get_env("AI_MODEL_DIR"), model_dir)

    if os.path.exists(save_dir):
        print(
            f"Tokenizer directory already exists: {save_dir}. Overwriting..."
        )
    os.makedirs(save_dir, exist_ok=True)

    tokenizer.save_pretrained(save_dir)
    print(f"Tokenizer saved to {save_dir}")

    return save_dir
