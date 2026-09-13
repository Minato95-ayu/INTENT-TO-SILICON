# Use official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AAYU_HOME=/app

# Create working directory
WORKDIR /app

# Install system dependencies if required for C/Rust FFI or extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY compiler/ ./compiler/
COPY runtime/ ./runtime/
COPY tools/ ./tools/

# Install the aayu-lang package
RUN pip install --no-cache-dir .

# Create a non-root user for security
RUN useradd -m aayu && chown -R aayu:aayu /app
USER aayu

# Default command
CMD ["aayu"]
