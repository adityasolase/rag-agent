from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.router import router  
import logging
import os


log_level = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level), format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


load_dotenv()
logger.info("Environment variables loaded.")


app = FastAPI(
    title="Natural Language RAG Agent",
    description="Backend for natural language portfolio queries powered by Cohere + LangChain",
    version="1.0.0"
)

frontend_urls = [
    "https://rag-agent-pi.vercel.app",
]

env_url = os.getenv("FRONTEND_URL")
if env_url:
    frontend_urls.append(env_url.rstrip('/'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_origin_regex=r"https://(.*\.)?vercel\.app",  
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400,  
)
logger.info("CORS middleware configured for frontend URLs: %s", frontend_urls)

app.include_router(router, prefix="/api")
logger.info("API router registered at /api")

@app.get("/")
def home():
    logger.info("Health check endpoint hit.")
    return {"message": "Backend is running "}

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app started successfully")
