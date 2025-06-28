import os
import requests
import logging
from dotenv import load_dotenv
from app.api.mongo_connector import get_all_clients, get_top_holders_from_mongo
from app.api.mysql_connector import get_top_holders, get_top_portfolios, get_manager_breakup
from app.api.response_format import format_response


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment!")


log_level = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level), format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def groq_chat(prompt: str, model="mixtral-8x7b-32768", temperature=0.7) -> str:
    try:
        logger.info("Sending request to Groq API...")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful wealth management assistant. If possible, respond in markdown table format."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }

        logger.debug(f"Groq Request Payload: {data}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        logger.info("Received response from Groq API.")
        return content

    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return f"Groq API Error: {e}"


def parse_table_from_groq_output(output: str):
    logger.debug("Attempting to parse table from Groq output.")
    lines = output.strip().split('\n')
    if len(lines) < 2 or "|" not in lines[0]:
        return None

    lines = [line for line in lines if not all(char in "-| " for char in line)]
    columns = [col.strip() for col in lines[0].split("|") if col.strip()]
    rows = []

    for line in lines[1:]:
        cells = [cell.strip() for cell in line.split("|") if cell.strip()]
        if len(cells) == len(columns):
            rows.append(cells)

    if columns and rows:
        logger.debug("Table parsing successful.")
        return format_response("table", columns=columns, rows=rows)
    return None


async def process_nl_query(query: str):
    try:
        logger.info(f"Processing query: {query}")
        query_lower = query.lower()

        
        if "holders of" in query_lower:
            stock = query_lower.split("holders of")[-1].strip()
            logger.info(f"Looking for holders of: {stock}")

            mysql_result = get_top_holders(stock)
            if mysql_result["labels"]:
                return format_response("chart", labels=mysql_result["labels"], data=mysql_result["data"])

            mongo_result = get_top_holders_from_mongo(stock)
            if mongo_result["labels"]:
                return format_response("chart", labels=mongo_result["labels"], data=mongo_result["data"])

            return format_response("text", f"No holders found for stock: {stock}")

        
        if "top" in query_lower and "portfolios" in query_lower:
            logger.info("Fetching top 5 portfolios...")
            top_clients = get_top_portfolios(limit=5)
            return format_response("table", columns=["Client"], rows=[[c] for c in top_clients])

        
        if "breakup" in query_lower and "manager" in query_lower:
            logger.info("Getting manager breakup...")
            managers = get_manager_breakup()
            return format_response(
                "chart",
                labels=[m["manager"] for m in managers],
                data=[m["value"] for m in managers]
            )

        
        if "client profiles" in query_lower:
            logger.info("Fetching client profiles...")
            profiles = get_all_clients()
            rows = [[p["name"], p["address"], p["risk_appetite"]] for p in profiles]
            return format_response("table", columns=["Name", "Address", "Risk"], rows=rows)

        
        if "top relationship manager" in query_lower:
            logger.info("Fetching top managers...")
            managers = get_manager_breakup()
            top = sorted(managers, key=lambda x: x["value"], reverse=True)[:3]
            return format_response("table", columns=["Manager", "Total Value"],
                                   rows=[[m["manager"], m["value"]] for m in top])

        
        logger.info("No match found. Using Groq fallback.")
        prompt = f"""You are an expert wealth management assistant. 
        Answer the following user query with business logic. 
        If relevant, use markdown tables.\n\nQuery: {query}"""

        output = groq_chat(prompt)

        if output.startswith("Groq API Error"):
            logger.warning(f"Groq failed. Returning fallback message for query: {query}")
            return format_response("text", "I couldn't find an answer. Please try rephrasing or ask something related to portfolios.")

        parsed = parse_table_from_groq_output(output)
        if parsed:
            return parsed

        return format_response("text", output)

    except Exception as e:
        logger.exception("Unhandled exception during query processing")
        return format_response("text", f"Error processing query: {str(e)}")
