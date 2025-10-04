#  Final Project – BuySmart: AI Shopping Site

**Course:** AI & Software Development Program  
**Instructor:** Matan Maman  
**Student:** Janna Glikshteyn  

---

##  Project Overview

**BuySmart** is a backend-focused e-commerce platform simulating a real-world online shopping system.  
It integrates **AI-powered assistance**, **secure authentication**, **data management**, and **interactive dashboards** — built entirely with **FastAPI**, **MySQL**, and **Streamlit**.

---

##  Features

- Full CRUD operations (Products, Customers, Orders, Payments, Wishlist)  
- AI Assistant powered by **OpenAI API**  
- JWT-based authentication & password hashing  
- Product search (by name and stock level)  
- Streamlit dashboard with dynamic graphs  
- Full API documentation  
- Dockerized deployment  
- Logging, error handling, and type hinting  

---

##  Technologies

| Category | Tools / Libraries |
|-----------|------------------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **Database** | MySQL |
| **Security** | JWT, Passlib (bcrypt) |
| **AI** | OpenAI API |
| **Frontend** | Streamlit |
| **Deployment** | Docker, Docker Compose |
| **Testing** | Postman |
| **Monitoring** | Logging, Type Hints, Error Handling |

---

##  Project Structure

BuySmart-AI_ShoppingSite/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── database.py # MySQL connection
│ ├── security.py # Password hashing & JWT
│ ├── gpt.py # OpenAI integration
│ ├── streamlit_app.py # Streamlit UI
│ ├── api_documentation.md # API reference
│ └── routers/ # All API routes
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── init_db.sql
└── README.md


---

##  Installation & Setup

### 1 Create Database
Make sure MySQL is installed or run via Docker:
```bash
CREATE DATABASE buysmart_db;

2️ Create .env file
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/buysmart_db
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key

3️ Run Locally
pip install -r requirements.txt
uvicorn backend.main:app --reload

4️ Run Streamlit UI
streamlit run backend/streamlit_app.py

5️ Run with Docker (recommended)
docker-compose up --build

 Security Highlights

Passwords hashed with bcrypt

JWT token authentication

Custom error handling and logging

Protected routes require Bearer token

 Search Features

Search products by full or partial name

Filter products by quantity (equal, greater, or less)

Reset filters easily in the Streamlit UI

 Streamlit Dashboards

Orders by month

Payments by method

Order status distribution

 API Testing

All endpoints were verified using Postman:

Category	Tested Routes
Authentication	/register, /login
CRUD Operations	Products, Customers, Orders, Payments, Wishlist
Validation	Error handling & token-based access
Instructor Requirements – Coverage Summary
#	Requirement	Status
1	FastAPI + MySQL
2	10+ Products in DB
3	Search by name & quantity
4	CRUD for all models
5	Password encryption (JWT + bcrypt)
6	OpenAI Integration
7	Docker Support
8	Streamlit UI
9	Graphs & Visuals
10	API Documentation
11	README File
12	Error Handling + Logging + Type Hints
13	Wishlist Feature

 Author's Note

This project represents a full cycle of learning — from backend logic to frontend visualization and deployment.
It combines creativity, problem-solving, and technical depth in one cohesive system.

Created and developed by Janna Glikshteyn
GitHub Repository - https://github.com/JannGerd/BuySmart--AI--ShoppingSite