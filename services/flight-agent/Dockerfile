# Build dalla ROOT del repo (serve libs/common e uv.lock):
#   docker build -f services/flight-agent/Dockerfile .
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

# 1) Solo i manifest del workspace: questo layer resta in cache finché non cambiano.
COPY pyproject.toml uv.lock ./
COPY libs/common/pyproject.toml libs/common/
COPY services/flight-agent/pyproject.toml services/flight-agent/
RUN uv sync --frozen --no-dev --package flight-agent --no-install-workspace

# 2) Codice: libreria comune + questo servizio
COPY libs/common/ libs/common/
COPY services/flight-agent/ services/flight-agent/
RUN uv sync --frozen --no-dev --package flight-agent

# Run as non-root
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Nessuna porta: l'agente parla solo con RabbitMQ (consuma flight.queue, pubblica su result.queue)
CMD ["python", "-m", "flight_agent.consumer"]
