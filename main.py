from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models
from routers import (admin, auth, blood_requests, donations, users)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BloodBridge API", description="Blood Donation & Emergency Assistance Platform", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://bloodbridge-frontend-1ryf.onrender.com"
],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blood_requests.router)
app.include_router(donations.router)
app.include_router(admin.router)

@app.get("/")
def root():

    return {"message": "Welcome to BloodBridge API"}


@app.get("/health")
def health_check():

    return {"status": "healthy"}

