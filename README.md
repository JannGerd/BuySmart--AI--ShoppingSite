🛒 BuySmart – AI-Powered Shopping Website

Final project for AI course.

📌 Project Overview

BuySmart is a backend API project for a simulated shopping site, developed as part of my final course project. The project focuses on backend development using FastAPI, SQLAlchemy, MySQL, and Streamlit for dashboard visualization.

The project includes a complete CRUD (Create, Read, Update, Delete) functionality for six key database tables:

Customers

Products

Orders

Payments

Order Items

User Wishlist

Additionally, it integrates OpenAI API (ChatGPT) for a demo AI assistant endpoint.

⚙️ Technologies Used

FastAPI for RESTful APIs

SQLAlchemy ORM for database connection

MySQL database

Pydantic for data validation

Docker for containerization

Streamlit for interactive dashboards and data visualization

OpenAI API (ChatGPT integration)

📂 Project Structure

backend/
├── routers/
│   ├── customers.py
│   ├── orders.py
│   ├── payments.py
│   ├── products.py
│   ├── order_items.py
│   ├── user_wishlist.py
│   └── gpt.py
├── models.py
├── schemas.py
├── database.py
├── main.py
├── auto_utils.py
└── streamlit_app.py

🧩 Key Features

Full CRUD APIs for all six tables

Dockerized setup

Streamlit dashboard with graphs:

Orders by month

Payments breakdown by method

(Additional graphs depending on data)

ChatGPT endpoint (/ask-gpt) for interacting with OpenAI API

🟢 How to Run

Backend API

uvicorn main:app --reload --host 127.0.0.1 --port 8000

Streamlit Dashboard

streamlit run streamlit_app.py

Docker (Optional)

docker-compose up --build

🧑‍💻 OpenAI API Integration

The /ask-gpt endpoint is connected to OpenAI's API using my assigned student key. Currently, due to quota limitations, this endpoint returns a response indicating insufficient quota. The code is functioning correctly and can be activated with a valid API key with sufficient credits.

✅ Current Project Status



🏁 Conclusion

This project was developed independently with attention to real-world backend skills and API integrations. Due to course limitations, certain external services (OpenAI GPT) are limited by credit balance but are technically functional.

Thank you for reviewing the project 🙏

💡 Author

This project was developed by me, as part of my Backend Developer course.

