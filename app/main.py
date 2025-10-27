
import os
from contextlib import asynccontextmanager

import torch
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from huggingface_hub import login
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from .auth import basic_auth

load_dotenv()

from .image_generator import generate_image, image_to_png_bytes
from .utilities import cleanup_memory as drop_cache
from .utilities import clear_buffer_cache


# * added the following so that watchman would keep the token in context
@asynccontextmanager
async def lifespan(app: FastAPI):
    token = os.getenv("HUGGING_FACE_HUB_TOKEN")
    if token:
        login(token=token)  # authenticate the child process
    yield
    drop_cache()
    clear_buffer_cache()

app = FastAPI(title="Image Server AI", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateReq(BaseModel):
    prompt: str
    guidance_scale: float = 4.0
    height: int = 768
    width: int = 768
    steps: int = 20

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/gpu-info")
def gpu_info():
    return {
        "cuda_available": torch.cuda.is_available(),
        "torch_cuda": getattr(torch.version, "cuda", None),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }

@app.post("/generate", dependencies=[Depends(basic_auth)])
async def generate(req: GenerateReq):
    img = await run_in_threadpool(
        generate_image, req.prompt, req.guidance_scale, req.height, req.width, req.steps
    )
    png = await run_in_threadpool(image_to_png_bytes, img)
    return Response(content=png, media_type="image/png")