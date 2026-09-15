from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import ApiInfoResponse, HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        env=settings.app_env,
        service=settings.app_name,
    )


@router.get("/", response_model=ApiInfoResponse, include_in_schema=True)
def api_info() -> ApiInfoResponse:
    settings = get_settings()
    return ApiInfoResponse(
        name=settings.app_name,
        version="v1",
        env=settings.app_env,
    )
