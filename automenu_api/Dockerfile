FROM python:3.12-alpine
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["fastapi", "run", "automenu_api/main.py", "--host", "0.0.0.0", "--port", "8000"]
