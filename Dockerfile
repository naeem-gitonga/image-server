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
ENV GENERATED_IMAGE_PATH=/app/app
ENV ENV=prod
ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "app"]