# 📚 Book Tracker API

A lightweight, self-hosted reading tracker built with FastAPI, PostgreSQL, and GitHub OAuth. Log books, track progress, and link to OpenLibrary — built as a hands-on project to explore Python backend development.

## 🚀 Features

- 📚 Add books with title, author, ISBN, or OLID
- 📈 Track reading progress (percent or pages)
- ✅ Mark books as want-to-read, in-progress, or completed
- 🔗 Automatically link to OpenLibrary for book covers and detail pages
- 🐳 Dockerized for self-hosted deployment
- 📄 OpenAPI docs auto-generated via FastAPI
- 🔐 GitHub OAuth authentication

## 📦 Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (via SQLModel)
- **Auth**: GitHub OAuth (via Authlib)
- **Migrations**: Alembic
- **API Server**: Uvicorn
- **Data Validation**: Pydantic
- **Database Driver**: psycopg2
- **Deployment**: Docker + Docker Compose

## 📐 Domain Model

```text
                  ┌──────────────┐
                  │    User      │
                  └──────────────┘
                          ▲
                          │ 1
                          │
                          │ N
                ┌────────────────────┐
                │   ReadingEntry     │
                └────────────────────┘
                │ id                 │
                │ user_id (FK)       │
                │ book_id (FK)       │
                │ start_date         │
                │ end_date           │
                │ progress (%)       │
                │ rating             │
                | review             │
                │ status             │
                └────────────────────┘
                          ▲
                          │ N
                          │
                          │ 1
                ┌────────────────────┐
                │       Book         │
                └────────────────────┘
                │ id                 │
                │ title              │
                │ author             │
                │ isbn / olid        │
                │ cover_url          │
                │ openlibrary_url    │
                └────────────────────┘
```

## 🛠 Prerequisites

- Python 3.13+
- Docker & Docker Compose (or Podman & Podman Compose) installed
- Git installed

## 🔑 Create .env

- Copy .env.example and fill required variables

## 🔧 Local Development

```bash
# Clone the project
git clone 
cd BookTrackerApi

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development DB
docker-compose up

# Run the app
uvicorn app.main:app --reload
```

## ✅ Project Roadmap

- [x] Setup project dependencies and virtual environment
- [x] Configure a database with Docker Compose (PostgreSQL)
- [x] Implement database connection and ORM models
- [ ] Define domain model (`User`, `Book`, `ReadingEntry`)
- [ ] Build API endpoints for book and reading progress management
- [ ] Integrate GitHub OAuth authentication
- [ ] Set up Alembic and create initial migration
- [ ] Add API rate limiting and security headers
- [ ] Create a Dockerfile for containerized deployment
