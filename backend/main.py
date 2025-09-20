from fastapi import FastAPI
from dotenv import load_dotenv
from backend.routers import auth
import os

from backend.database import create_tables
from backend.routers import customers, products, orders, payments, user_wishlist
import backend.gpt as gpt

load_dotenv()
app = FastAPI(title="BuySmart API")
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(user_wishlist.router)
app.include_router(gpt.router)

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "ברוכים הבאים ל־BuySmart!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
