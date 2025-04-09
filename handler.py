"""
This is very basic handler for Flux images.
It uses random seed and always generates a square image.
You need to have HF_TOKEN in the environment.
"""

import torch
from diffusers import FluxPipeline
from huggingface_hub import login
import os
import runpod
import io
import base64
from PIL import Image

# Load Hugging Face token from the environment.
# Although the model should be cached in the Docker image,
# you may still need the token too. Not sure.
hf_token = os.environ.get("HF_TOKEN")
login(token = hf_token)

# Load the model and reuse for all requests.
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload() # Save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power.

def pil_to_base64_png(image: Image.Image) -> str:
    """Converts a PIL image data to a base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64

@torch.inference_mode()
def generate_image(job):
    """This handler function assumes the prompt to be
    in prompt property in the input. If there is an exception,
    returns empty string instead of a base64 string."""

    try:
        prompt = job["input"]["prompt"]

        image = pipe(
            prompt,
            height=1024,
            width=1024,
            guidance_scale=3.5,
            num_inference_steps=20,
            max_sequence_length=512
        ).images[0]

        # Convert to base64
        image_str = pil_to_base64_png(image)
        image_url = f"data:image/png;base64,{image_str}"

        result = {
            "image_url": image_url
        }

        return result
    except Exception as err:
        print("Exception during image generation:")
        print(err)

        result = {
            "image_url": ""
        }

        return result

runpod.serverless.start({"handler": generate_image})
