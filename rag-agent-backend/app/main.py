from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.router import router  #Modular API router
import logging
import os

#Setup logging
log_level = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level), format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

#Load environment variables from .env file
load_dotenv()
logger.info("Environment variables loaded.")

#Create FastAPI app instance
app = FastAPI(
    title="Natural Language RAG Agent",
    description="Backend for natural language portfolio queries powered by Cohere + LangChain",
    version="1.0.0"
)

#Enable CORS for frontend (React running on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured for http://localhost:3000")

#Register API routes
app.include_router(router, prefix="/api")
logger.info("API router registered at /api")

#Health check route
@app.get("/")
def home():
    logger.info("Health check endpoint hit.")
    return {"message": "Backend is running "}

#Optional startup event logging
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app started successfully")
