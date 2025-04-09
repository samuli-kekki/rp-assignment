"""
This script is used to preload the model into the Docker image.
You need to have HF_TOKEN in the environment.
"""

import torch
from diffusers import FluxPipeline
from huggingface_hub import login
import os

def load_model():
    # To preload the model, we need Hugging Face token.
    # I think the RunPod GitHub integration build machine
    # does not support specifying environment variables,
    # so this may not work today.
    hf_token = os.environ.get("HF_BUILD_TOKEN")
    if not hf_token:
        print("Error: no HF_BUILD_TOKEN!")
        return

    login(token = hf_token)

    # Load the model in order to download it into the cache in the Docker image
    _ = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)

if __name__ == "__main__":
    load_model()
