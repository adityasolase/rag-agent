from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.langchain_agent import process_nl_query
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
async def handle_query(request: QueryRequest):
    query_text = request.query.strip()

    if not query_text:
        logger.warning("Received empty query.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    logger.info(f"Handling user query: {query_text}")

    try:
        
        response = await process_nl_query(query_text)
        logger.info(f"Successfully processed query.")
        return response

    except Exception as e:
        logger.exception("Error while processing query")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
