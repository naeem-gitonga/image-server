FROM nvcr.io/nvidia/pytorch:25.09-py3-igpu

ENV PATH="/root/.local/bin:${PATH}"
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev 

COPY . .

ENV PATH="/app/.venv/bin:${PATH}"
ENV MODEL_DIR=/models
ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1"]
