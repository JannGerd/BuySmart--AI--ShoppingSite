🛒 BuySmart – AI-Powered Shopping Website

Final project for AI course.


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


## ⚙️ Technologies Used
- FastAPI for RESTful APIs  
- SQLAlchemy ORM for database connection  
- MySQL database  
- Pydantic for data validation  
- Docker for containerization  
- Streamlit for interactive dashboards and data visualization  
- OpenAI API (ChatGPT integration)


## 📂 Project Structure

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



## 🧩 Key Features
- Full CRUD APIs for all six tables  
- Dockerized setup  
- Streamlit dashboard with graphs:  
  - Orders by month  
  - Payments breakdown by method  
  - (Additional graphs depending on data)  
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


🧑‍💻 OpenAI API Integration

The /ask-gpt endpoint is connected to OpenAI's API.
Currently, due to quota limitations, this endpoint returns a response indicating insufficient quota.
The code is functioning correctly and can be activated with a valid API key with sufficient credits.

✅ Current Project Status

The project runs successfully in both local and Docker environments.
All required features for backend CRUD, API endpoints, and Streamlit dashboard are implemented.

🏁 Conclusion

This project was developed independently with attention to real-world backend skills and API integrations.
Due to course limitations, certain external services (OpenAI GPT) are limited by credit balance but are


💡 Author
This project was developed by me as part of my Backend Developer course.

