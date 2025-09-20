# 🛒 BuySmart – AI-Powered Shopping Website

Final project for AI course.

---

## 📌 Project Overview
BuySmart is a backend API project for a simulated shopping site, developed as part of my final course project.  
The project focuses on backend development using **FastAPI**, **SQLAlchemy**, **MySQL**, and **Streamlit** for dashboard visualization.

The project includes complete CRUD (Create, Read, Update, Delete) functionality for six key database tables:

- Customers  
- Products  
- Orders  
- Payments  
- Order Items  
- User Wishlist  

Additionally, it integrates **OpenAI API (ChatGPT)** for a demo AI assistant endpoint.

---

## ⚙️ Technologies Used
- FastAPI for RESTful APIs  
- SQLAlchemy ORM for database connection  
- MySQL database  
- Pydantic for data validation  
- Docker for containerization  
- Streamlit for interactive dashboards and data visualization  
- OpenAI API (ChatGPT integration)  

---

## 📂 Project Structure
```
backend/
├── routers/
│ ├── customers.py
│ ├── orders.py
│ ├── payments.py
│ ├── products.py
│ ├── order_items.py
│ ├── user_wishlist.py
│ └── gpt.py
├── models.py
├── schemas.py
├── database.py
├── main.py
├── auto_utils.py
└── streamlit_app.py

init_db.sql
requirements.txt
.env.example
docker-compose.yml (optional)
```

## 🧩 Key Features
- Full CRUD APIs for all six tables  
- Dockerized setup  
- Authentication with JWT (register, login, logout, delete user)  
- Password hashing with bcrypt  
- Protected routes for Orders, Wishlist, and User actions  
- Streamlit dashboard with:  
  - Orders by month  
  - Payments breakdown by method  
  - Product, Orders and Wishlist views  
  - Login/Register and Chat Assistant (integrated with ChatGPT API)  
- ChatGPT endpoint (`/ask-gpt`) for interacting with OpenAI API  


## 🟢 How to Run

### Local setup (without Docker)
```bash
git clone https://github.com/JannGerd/BuySmart--AI--ShoppingSite
cd BuySmart--AI--ShoppingSite

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy example environment file
cp .env.example .env

# Initialize database schema (requires MySQL running locally)
mysql -u root -p < init_db.sql

# Run backend API
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000


API Docs → http://127.0.0.1:8000/docs
Health Check → http://127.0.0.1:8000/healthz

streamlit run streamlit_app.py

cp .env.example .env
# Make sure DATABASE_URL in .env points to "db" host:
# DATABASE_URL=mysql+pymysql://buysmart:buysmart123@db:3306/buysmart
docker-compose up --build


API → http://localhost:8000/docs
Streamlit → http://localhost:8501
```

📝 Note

The Streamlit UI is minimal – intended for demo and visualization, not production frontend.

ChatGPT API integration is implemented but currently limited due to API quota.

Bonus ML feature (prediction model) was not implemented as it was optional.

✅ Current Project Status & Conclusion

The project runs successfully in both local and Docker environments.
All required features for backend CRUD, authentication, API endpoints, and Streamlit dashboard are implemented.

This project was developed independently with attention to real-world backend skills and API integrations.
OpenAI GPT integration is functional but limited due to credit quota.
Overall, the project demonstrates a complete end-to-end system with a strong backend focus.