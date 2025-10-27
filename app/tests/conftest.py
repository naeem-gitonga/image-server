import pytest
import torch


# * use this file for shared fixtures 
# @pytest.fixture
# def mock_cuda():
#     def _mock(monkeypatch, available=False, name="NVIDIA GB10"):
#         # Mock cuda availability
#         monkeypatch.setattr(torch.cuda, "is_available", lambda: available)
        
#         if available:
#             # Mock CUDA being available
#             monkeypatch.setattr(torch.cuda, "device_count", lambda: 1)
#             monkeypatch.setattr(torch.cuda, "get_device_name", lambda idx: name)
#             monkeypatch.setattr(torch.cuda, "get_device_properties", 
#                             lambda idx: type('obj', (object,), {
#                                 'total_memory': 8589934592,  # 8GB in bytes
#                                 'name': 'Mocked GPU',
#                                 'torch_cuda': '12.9'
#                             })())
#             monkeypatch.setattr(torch.version, "cuda", "12.9")
#         else:
#             # Mock CUDA not being available
#             monkeypatch.setattr(torch.cuda, "device_count", lambda: 0)
#             monkeypatch.setattr(torch.version, "cuda", None)
#     return _mock