from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
def ready() -> dict[str, str]:
    # Current endpoints have no remote dependency; model readiness belongs here later.
    return {"status": "ready"}
