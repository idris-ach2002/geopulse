"""GeoPulse FastAPI entrypoint."""

from fastapi import FastAPI

app = FastAPI(
    title="GeoPulse API",
    version="0.0.1",
)


@app.get("/health/live")
async def health_live() -> dict[str, str]:
    """Return process liveness."""
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready() -> dict[str, str]:
    """Return V0 readiness."""
    return {"status": "ready"}
