FROM nvcr.io/nvidia/pytorch:25.09-py3

WORKDIR /app

RUN pip install fastapi uvicorn[standard] \
    pydantic python-multipart \
    pillow diffusers transformers \
    huggingface \
    peft \
    sentencepiece

COPY . .

ENV MODEL_DIR=/models
ENV PORT=80
EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]