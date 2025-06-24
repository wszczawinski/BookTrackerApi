# 📚 Book Tracker API

A lightweight, self-hosted reading tracker built with FastAPI, PostgreSQL, and GitHub OAuth. Log books, track progress, and link to OpenLibrary — built as a hands-on project to explore Python backend development.

## 🚀 Features

- 🔐 GitHub OAuth authentication
- 📚 Add books with title, author, ISBN, or OLID
- 📈 Track reading progress (percent or pages)
- ✅ Mark books as started, in-progress, or finished
- 🔗 Automatically link to OpenLibrary for book covers and detail pages
- 🐳 Dockerized for self-hosted deployment
- 📄 OpenAPI docs auto-generated via FastAPI


## 📦 Tech Stack

- **Backend**: FastAPI
- **Auth**: GitHub OAuth (via Authlib)
- **Database**: PostgreSQL (via SQLAlchemy)
- **Migrations**: Alembic
- **External API**: OpenLibrary (for metadata)
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
- [ ] Configure a database with Docker Compose (PostgreSQL)
- [ ] Implement database connection and ORM models
- [ ] Set up Alembic and create initial migration
- [ ] Define domain model (`User`, `Book`, `ReadingEntry`)
- [ ] Integrate GitHub OAuth authentication
- [ ] Create a Dockerfile for containerized deployment
- [ ] Build API endpoints for book and reading progress management
