from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import LoginApi
from api import KriteriaApi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SPK WSM"}

app.include_router(LoginApi.router, prefix="/api")
app.include_router(KriteriaApi.router, prefix="/api")
