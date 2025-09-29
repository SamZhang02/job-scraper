FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy your lock + project files
COPY pyproject.toml uv.lock ./

# Install using uv (system mode to avoid venv inside Docker)
RUN uv pip install --system .

COPY . .

CMD ["python", "-m", "App.main"]
