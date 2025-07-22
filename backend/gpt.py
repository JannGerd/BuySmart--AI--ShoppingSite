from openai import OpenAI
from fastapi import APIRouter, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/ask-gpt")
def ask_gpt(request_data: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request_data.prompt}]
        )
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = f"שגיאה בפנייה ל-GPT: {str(e)}. כרגע לא ניתן לקבל תשובה, נסי מאוחר יותר."

    return {"response": response}