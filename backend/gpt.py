from openai import OpenAI
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI router
router = APIRouter()


# Request schema
class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt for GPT")


@router.post("/ask-gpt", response_model=dict)
def ask_gpt(request_data: ChatRequest) -> JSONResponse:
    """
    Send a user prompt to OpenAI's GPT-3.5-turbo model and return the generated response.

    Args:
        request_data (ChatRequest): A Pydantic model containing the user prompt.

    Returns:
        JSONResponse: A dictionary containing the GPT model's response.
    """
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request_data.prompt}]
        )
        response = chat_completion.choices[0].message.content
        logger.info("GPT response returned successfully.")
        return JSONResponse(content={"response": response}, status_code=200)

    except Exception as e:
        logger.exception("GPT request failed.")
        return JSONResponse(
            content={"response": f"שגיאה בפנייה ל-GPT: {str(e)}. כרגע לא ניתן לקבל תשובה, נסי מאוחר יותר."},
            status_code=500
        )
