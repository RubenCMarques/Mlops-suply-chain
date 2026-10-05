from fastapi import FastAPI

from supply_chain.api.routes import health, system


def create_app() -> FastAPI:
    app = FastAPI(title="Supply Chain API", version="0.1.0")
    app.include_router(health.router)
    app.include_router(system.router)
    return app


app = create_app()
