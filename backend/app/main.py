from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
from app.api import records, students, teachers

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefix
app.include_router(records.router, prefix='/records')
# app.include_router(records.router, prefix="/api")
app.include_router(students.router, prefix='/students')
app.include_router(teachers.router, prefix='/teachers')