# SalesPilot AI CRM

A modern, complete sales CRM built with FastAPI, MySQL, and a beautiful human-written UI.

## Features
- **Auth**: JWT-based authentication (works with both API and Web UI).
- **Leads Management**: Track leads, score them, and manage statuses.
- **Deals Pipeline**: Kanban-style board to track revenue stages.
- **Customers**: Convert leads to customers.
- **Follow-ups**: Schedule reminders.
- **AI Sales Assistant**: Generate personalized cold pitches, follow-ups, and get lead score explanations (currently mocked for 100% free local execution).
- **Dashboard**: Key metrics at a glance.

## Prerequisites
- Python 3.10+
- MySQL Server (running on localhost:3306)

## Setup Instructions

1. **Database Setup**
   Ensure MySQL is running. Create the database:
   ```sql
   CREATE DATABASE salespilot;
   ```
   *Note: If your MySQL root user has a different password than `password`, please update the `.env` file accordingly.*

2. **Virtual Environment & Dependencies**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Database Migrations**
   Initialize the database schema using Alembic:
   ```bash
   alembic revision --autogenerate -m "Initial schema"
   alembic upgrade head
   ```

4. **Seed Data**
   Populate the database with a demo user and sample data:
   ```bash
   python seed.py
   ```

5. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Login**
   - **URL:** http://127.0.0.1:8000
   - **Email:** demo@salespilot.io
   - **Password:** demo1234
