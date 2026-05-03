FROM python:3.12.3-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

FROM python:3.12.3-slim-bookworm AS production

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser certificates ./certificates
COPY --chown=appuser:appuser entrypoint.sh ./entrypoint.sh
COPY --chown=appuser:appuser entrypoint-worker.sh ./entrypoint-worker.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

RUN chmod +x ./entrypoint.sh ./entrypoint-worker.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["sh", "-c", "exec uvicorn main:app --host ${APP_CONFIG__RUN__HOST:-0.0.0.0} --port ${APP_CONFIG__RUN__PORT:-8000}"]
