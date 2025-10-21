FROM nvcr.io/nvidia/pytorch:25.09-py3

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev --venv=${VIRTUAL_ENV}

COPY . .

ENV PATH="/app/.venv/bin:${PATH}"
ENV MODEL_DIR=/models
ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
