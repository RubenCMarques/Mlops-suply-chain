from fastapi import FastAPI

from supply_chain.api.routes import health, system


def create_app() -> FastAPI:
    application = FastAPI(title="Supply Chain API", version="0.1.0")
    application.include_router(health.router)
    application.include_router(system.router)
    return application


app = create_app()
