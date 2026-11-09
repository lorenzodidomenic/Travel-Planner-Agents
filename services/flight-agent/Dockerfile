FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Node.js/npm: needed only if some MCP servers are launched with npx.
# Remove this block if every MCP server is Python-based.
RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv binary (pinned) for fast, reproducible dependency installs
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

WORKDIR /app

# 1) Dependencies first, so this layer is cached until pyproject/uv.lock change.
#    uv.lock* is optional: the build works even before a lock file exists.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project

# 2) Application code
COPY src/ ./src/

# Run as non-root
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "flight_agent.api:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
