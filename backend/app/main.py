from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict
from app.config import API_TITLE, API_VERSION, ALLOWED_HOSTS

app = FastAPI(title=API_TITLE, version=API_VERSION)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, tags=["prediction"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {API_TITLE}", "status": "online"}
