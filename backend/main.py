from fastapi import FastAPI
from backend.database import create_tables
from backend.routers import customers, products, orders, payments, user_wishlist
import backend.gpt as gpt

from dotenv import load_dotenv
import os
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI(title="BuySmart API")

create_tables()

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(user_wishlist.router)
app.include_router(gpt.router)


@app.get("/")
def root():
    return {"message": "ברוכים הבאים ל־BuySmart!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)