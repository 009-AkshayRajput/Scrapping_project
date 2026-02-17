# Groww Stock Scraper API

A FastAPI-based backend application that scrapes Top Volume Stocks from Groww and stores them in a MySQL database.

# Features

- Scrapes stock data from Groww (Top Volume page)
- Stores data in MySQL
- Updates existing records (no duplicates)
- REST API built using FastAPI
- Swagger UI for API testing
- Async-compatible architecture

# Tech Stack
**- FastAPI**
**- Playwright (Sync API)**
**- MySQL**
**- SQLAlchemy ORM**
**- Uvicorn**

# Setup Instructions
**1- Clone the Repository**
git clone <your-repo-url>
cd scrapping_project

**2️- Create Virtual Environment**
- python -m venv venv
- venv\Scripts\activate

**3- Install Dependencies**
- pip install -r requirements.txt


**If Playwright browsers are not installed:**
- playwright install

**4️- Configure Database**
- Update your database.py:
- DATABASE_URL = "mysql+pymysql://username:password@localhost/stock_db"


**Make sure MySQL database exists:**
- CREATE DATABASE stock_db;

**5️- Run the Server**
- uvicorn app.main:app --reload


**Server will start at:**
- http://127.0.0.1:8000

# API Endpoints
**Login**
- POST /auth/login

**Scrape Stocks**
- POST /scrape/

**Example Response:**
{
  "message": "Scraping completed successfully",
  "new_records": 50,
  "existing_records": 0,
  "total_scraped": 50
}

**API Documentation**
Swagger UI available at:
- http://127.0.0.1:8000/docs

**How Scraping Works**
Opens Groww Top Volume page using Playwright
Extracts:
Company Name
Price
Volume

**Checks if stock already exists:**
If exists → Updates record
If not → Inserts new record
Returns summary response

**Design Decisions**
- Used Playwright because Groww loads data dynamically.
- Used sync Playwright inside threadpool to avoid Python asyncio subprocess issues.
- Used unique constraint on company_name to prevent duplicates.
- Implemented update logic for existing records.

# Author
- Akshay Rajput



