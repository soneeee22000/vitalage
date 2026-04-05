import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded

from src.agents.mistral_utils import AgentError, AgentTimeoutError
from src.api.v1.auth import router as auth_router
from src.api.v1.check_ins import router as check_ins_router
from src.api.v1.habits import router as habits_router
from src.api.v1.health import router as health_router
from src.api.v1.insights import router as insights_router
from src.api.v1.meals import router as meals_router
from src.api.v1.vitality import router as vitality_router
from src.config.settings import settings
from src.db.engine import engine
from src.middleware.auth import verify_token
from src.middleware.rate_limit import get_rate_limit_key

logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_rate_limit_key,
    enabled=settings.rate_limit_enabled,
)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Create tables on startup and dispose engine on shutdown."""
    from src.db import tables as _tables  # noqa: F401
    from src.db.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables recreated")
    yield
    await engine.dispose()


app = FastAPI(
    title="VitalAge API",
    description="Daily vitality companion for smart aging",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """Handle rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Trop de requetes. Veuillez patienter avant de reessayer.",
            "code": "RATE_LIMIT_EXCEEDED",
        },
    )


@app.exception_handler(AgentTimeoutError)
async def agent_timeout_handler(
    request: Request, exc: AgentTimeoutError
) -> JSONResponse:
    """Handle AI agent timeout errors."""
    logger.warning("Agent timeout: %s", exc)
    return JSONResponse(
        status_code=504,
        content={
            "detail": "Le service d'analyse est temporairement lent. Reessayez.",
            "code": "AI_TIMEOUT",
        },
    )


@app.exception_handler(AgentError)
async def agent_error_handler(request: Request, exc: AgentError) -> JSONResponse:
    """Handle AI agent errors."""
    logger.error("Agent error: %s", exc)
    return JSONResponse(
        status_code=502,
        content={
            "detail": "Le service d'analyse est temporairement indisponible.",
            "code": "AI_UNAVAILABLE",
        },
    )


app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(
    check_ins_router, prefix="/api/v1", dependencies=[Depends(verify_token)]
)
app.include_router(
    meals_router, prefix="/api/v1", dependencies=[Depends(verify_token)]
)
app.include_router(
    vitality_router, prefix="/api/v1", dependencies=[Depends(verify_token)]
)
app.include_router(
    habits_router, prefix="/api/v1", dependencies=[Depends(verify_token)]
)
app.include_router(
    insights_router, prefix="/api/v1", dependencies=[Depends(verify_token)]
)

STATIC_DIR = Path(__file__).parent.parent / "static"

if STATIC_DIR.exists():
    assets_dir = str(STATIC_DIR / "assets")
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str) -> FileResponse:
        """Serve the SPA frontend for all non-API routes."""
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))
