from fastapi import FastAPI

app = FastAPI(
    title="GeoPulse API",
    version="0.0.1",
)


@app.get("/health/live")
async def health_live() -> dict[str, str]:
    """Return the liveness status of the API process."""
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready() -> dict[str, str]:
    """Return the readiness status.

    V0 has no external mandatory dependency yet.
    """
    return {"status": "ready"}
