from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, question, answer, user_quest

# Create FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,  # Allow sending cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(question.router, prefix="/questions", tags=["questions"])
app.include_router(answer.router, prefix="/answers", tags=["answers"])
app.include_router(user_quest.router, prefix="/user_quests", tags=["user_quests"])

