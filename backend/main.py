from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import user_routes

app = FastAPI()

# 🔥 CORS MUST BE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1.5500"
    ],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 ROUTES AFTER CORS
app.include_router(user_routes.router)


@app.get("/")
def home():
    return {"message": "AI Energy System Running"}