from ..utils import get_env
from transformers import MBartForConditionalGeneration
import torch
import os


def load_model(
    model_name: str = "facebook/mbart-large-50-many-to-many-mmt", device: str = None
) -> MBartForConditionalGeneration:
    """
    Load a model from the Hugging Face model hub
    """
    try:
        if not device:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        model = MBartForConditionalGeneration.from_pretrained(model_name)
        model.to(device)
    except Exception as e:
        print(f"Error loading model")
        raise e

    return model


def save_model(model: MBartForConditionalGeneration, model_name: str) -> str:
    """
    Save a model to the output directory
    """

    model_dir = f"model_{model_name}"
    save_dir = os.path.join(get_env("AI_MODEL_DIR"), model_dir)

    if os.path.exists(save_dir):
        print(f"Model directory already exists: {save_dir}. Overwriting...")
    os.makedirs(save_dir, exist_ok=True)

    model.save_pretrained(save_dir)
    print(f"Model saved to {save_dir}")

    return save_dir

if __name__ == "__main__":
    model = load_model()
    save_model(model, "test_save")