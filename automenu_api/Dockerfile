FROM python:3.12-slim

WORKDIR /app

RUN pip install uv
# Install in the way recommended by the documentation.

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
# Multi-stage build: separate preparing dependencies from pulling a finished environment from the runtime.

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1
# Add a 'ready' endpoint.

CMD ["uvicorn", "automenu_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
