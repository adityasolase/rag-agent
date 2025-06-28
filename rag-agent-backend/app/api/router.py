from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.langchain_agent import process_nl_query
import logging

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

router = APIRouter()

# Pydantic model to validate incoming request
class QueryRequest(BaseModel):
    query: str

# POST endpoint to handle natural language queries
@router.post("/query")
async def handle_query(request: QueryRequest):
    query_text = request.query.strip()

    if not query_text:
        logger.warning("Received empty query.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    logger.info(f"Handling user query: {query_text}")

    try:
        # Call the LangChain agent or fallback
        response = await process_nl_query(query_text)
        logger.info(f"Successfully processed query.")
        return response

    except Exception as e:
        logger.exception("Error while processing query")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
