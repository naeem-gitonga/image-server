import builtins
import io
import os
import types
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from PIL import Image

from app.auth import basic_auth
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

# def test_health_ok(client):
#     r = client.get("/health")
#     assert r.status_code == 200
#     assert r.json() == {"ok": True}

def test_gpu_info_cpu(monkeypatch, client, mock_cuda):
    mock_cuda(monkeypatch, available=False)
    r = client.get("/gpu-info")
    assert r.status_code == 200
    data = r.json()
    assert data["cuda_available"] is False
    assert data["torch_cuda"] is None
    assert data["device"] == "cpu"

# def test_gpu_info_gpu(monkeypatch, client, mock_cuda):
#     mock_cuda(monkeypatch, available=True, name="NVIDIA GB10")
#     r = client.get("/gpu-info")
#     assert r.status_code == 200
#     data = r.json()
#     assert data["cuda_available"] is True
#     assert data["torch_cuda"] == "12.9"
#     assert data["device"] == "NVIDIA GB10"

# def test_generate_ok(client):
#     payload = {
#         "prompt": "a sunrise over mountains",
#         "guidance_scale": 3.5,
#         "height": 256,
#         "width": 256,
#         "steps": 5,
#     }
#     fake_img = Image.new('RGB', (256, 256), color='red')
    
#     # Mock the generate_image function to return our fake image
#     with patch('app.main.generate_image', return_value=fake_img):
#         r = client.post("/generate", json=payload, auth=("admin", "secret123"))
    
#     assert r.status_code == 200
#     assert r.headers["content-type"] == "image/png"
#     assert r.content.startswith(b"\x89PNG")

# def test_generate_unauthorized(client):
#     r = client.post("/generate", json={"prompt": "x"})
#     assert r.status_code == 401