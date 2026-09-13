from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import admin, churn, customers, exports, health, portfolio, propensity
from backend.app.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(portfolio.router, prefix=settings.api_prefix)
    app.include_router(churn.router, prefix=settings.api_prefix)
    app.include_router(propensity.router, prefix=settings.api_prefix)
    app.include_router(customers.router, prefix=settings.api_prefix)
    app.include_router(exports.router, prefix=settings.api_prefix)
    app.include_router(admin.router, prefix=settings.api_prefix)

    return app


app = create_app()

