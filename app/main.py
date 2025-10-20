
import torch
import json, sys, subprocess
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .auth import maybe_basic_auth
from dotenv import load_dotenv
import gc
from contextlib import asynccontextmanager
from huggingface_hub import login

load_dotenv() 

from fastapi.responses import Response, StreamingResponse
from starlette.concurrency import run_in_threadpool

from .image_generator import generate_image, image_to_png_bytes

# * added the following so that watchman would keep the token in context
@asynccontextmanager
async def lifespan(app: FastAPI):
    token = os.getenv("HUGGING_FACE_HUB_TOKEN")
    if token:
        login(token=token)  # authenticate the child process
    yield


app = FastAPI(title="FastAPI Code Runner (uv)", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    code: str = Field(..., description="Python code to execute")
    stdin: Optional[str] = Field("", description="Optional stdin for the code")
    timeout_sec: int = Field(2, ge=1, le=30, description="Wall-clock timeout in seconds")
    mem_limit_mb: int = Field(256, ge=64, le=2048, description="Memory limit in MB")

class RunResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    time_ms: int

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

@app.post("/generate", dependencies=[Depends(maybe_basic_auth)])
async def generate(req: GenerateReq):
    img = await run_in_threadpool(
        generate_image, req.prompt, req.guidance_scale, req.height, req.width, req.steps
    )
    png = await run_in_threadpool(image_to_png_bytes, img)
    return Response(content=png, media_type="image/png")

@app.on_event("shutdown")
def cleanup_memory():
    print("[CLEANUP] Releasing model + RAM...")
    try:
        from app.image_generator import _pipeline
        _pipeline = None
    except:
        pass

    gc.collect()

    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except:
        pass
    print("[CLEANUP] Done!")