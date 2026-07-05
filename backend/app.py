from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.vector_routes import router as vector_router

app = FastAPI(title="VeraDB")

# Configure CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],  # Allows your frontend server port
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)

# Include your routes
app.include_router(vector_router)