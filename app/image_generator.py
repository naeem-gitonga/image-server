import os
import torch
from io import BytesIO
from typing import Optional
from diffusers import AutoPipelineForText2Image
from PIL import Image
from threading import Lock
from dotenv import load_dotenv
load_dotenv()

_pipeline = None
_lock = Lock()  # * simple guard for single-GPU concurrency

print("CUDA:", torch.cuda.is_available(),
      "Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "-",
      "CUDA tag:", torch.version.cuda
)

def _init_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    pipe = None
    if torch.cuda.is_available():
        print("\n\n\nCUDA IS RUNNING!!\n\n\n")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "./models/flux",
            use_safetensors=True,
            dtype=torch.bfloat16,
            device_map="cuda", 
        )

        pipe.load_lora_weights(
            "./models/lora",
            use_peft_backend=True,
            adapter_name="v1",
        )
        # pipe.enable_attention_slicing()
        # pipe.enable_model_cpu_offload()
    else:
        print("\n\n\nRUNNING ON CPU ONLY\n\n\n")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "./models/flux",
            use_safetensors=True,
        )

        pipe.load_lora_weights(
            "./models/lora",
            use_peft_backend=True,
            adapter_name="v1",
        )

    pipe.set_adapters(["v1"], adapter_weights=[1.0])    

    _pipeline = pipe
    return _pipeline

def generate_image(
        prompt: str,
        guidance_scale: float = 4.0,
        height: int = 768,
        width: int = 768,
        steps: int = 20
    ) -> Image.Image:
    pipe = _init_pipeline()

    with _lock:       # * Prevent overlapping forward passes on a single GPU
        image = pipe(
            prompt=prompt,
            guidance_scale=guidance_scale,
            height=height,
            width=width,
            num_inference_steps=steps,
        ).images[0]
        image.save("pic.png")
    return image

def image_to_png_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
