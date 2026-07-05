from fastapi import FastAPI

from backend.routes.vector_routes import router


app = FastAPI(
    title="VeraDB",
    version="1.0"
)

app.include_router(router)