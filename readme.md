# 📚 Book Tracker API

A lightweight, self-hosted reading tracker built with FastAPI, PostgreSQL, and GitHub OAuth. Log books, track progress, and link to OpenLibrary — built as a hands-on project to explore Python backend development.

## 🚀 Features

- 📚 Add books with title, author, ISBN, or OLID
- 📈 Track reading progress (percent or pages)
- ✅ Mark books as want-to-read, in-progress, or completed
- 🔗 Automatically link to OpenLibrary for book covers and detail pages
- 🐳 Dockerized for self-hosted deployment
- 📄 OpenAPI docs auto-generated via FastAPI
- 🔐 Supabase OAuth authentication with secure HTTP-only cookies

## 📦 Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (via SQLModel)
- **Auth**: Supabase OAuth with HTTP-only cookies
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

## 🔐 Authentication Flow

This API uses Supabase for OAuth authentication with secure HTTP-only cookies. Here's how it works:

```text
Frontend                    Your API                 Supabase
   |                          |                        |
   |-- Supabase Auth --------------------------------->|
   |<--- Supabase JWT ---------------------------------|
   |                          |                        |
   |-- POST /auth/login ----->|                        |
   |   (Supabase JWT)         |-- Validate JWT ------->|
   |                          |<-- Valid --------------|
   |                          |-- Generate API JWT ----|
   |<-- Set-Cookie: API JWT --|                        |
   |                          |                        |
   |-- GET /books ----------->|                        |
   |   (Cookie: API JWT)      |-- Validate API JWT ----|
   |                          |<-- Valid (no external) |
   |<-- Books data -----------|                        |
   |                          |                        |
   |-- POST /auth/refresh --->|                        |
   |   (Cookie: API JWT)      |-- Generate NEW JWT ----|
   |<-- Set-Cookie: NEW JWT --|                        |
   |                          |                        |
   |-- DELETE /auth/logout -->|                        |
   |<-- Clear Cookie ---------|                        |
```

### API Endpoints

- `POST /api/v1/auth/login` - Exchange Supabase JWT for your own API JWT cookie
- `POST /api/v1/auth/refresh` - Refresh API JWT token (24h expiry)
- `GET /api/v1/auth/me` - Get current user info
- `DELETE /api/v1/auth/logout` - Clear authentication cookie

### Security Features

- **Dual JWT strategy** - API generates its own JWT, Supabase JWT only used for initial login
- **HTTP-only cookies** - JavaScript cannot access API tokens (XSS protection)
- **Environment-aware security** - HTTPS-only cookies in production, HTTP allowed in development
- **Short token lifetime** - 24-hour expiry with refresh capability
- **Stateless authentication** - No server-side sessions, fully scalable
- **Secure cookie flags** - `httponly=True`, `secure=production`, `samesite=lax`
- **Token validation** - Proper JWT signature, issuer, and expiry verification
- **Token revocation** - Change API_JWT_SECRET to invalidate all tokens instantly

### Security Model

1. **Supabase validation**: Supabase JWT validated once during login with proper audience check
2. **Token exchange**: API generates its own JWT (24h expiry) with custom issuer
3. **Secure storage**: API JWT stored in HTTP-only cookie with security flags
4. **Memory cleanup**: Frontend clears Supabase JWT from memory after login
5. **Independent auth**: API validates its own tokens locally, zero external dependencies
6. **Refresh capability**: Frontend can refresh tokens before expiry using existing cookie
7. **Complete control**: You manage the entire token lifecycle and can revoke instantly
8. **Error handling**: Graceful JWT validation with proper error responses

### Why This Approach?

- **Best of both worlds**: Leverage Supabase OAuth complexity while maintaining control
- **Enhanced security**: Shorter-lived tokens (24h) with refresh capability
- **Stateless design**: No server sessions, horizontally scalable
- **Independence**: Your API doesn't depend on Supabase for ongoing authentication
- **Flexibility**: Easy to add features like token revocation, audit trails, etc.

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

### ✅ Completed

- [x] Setup project dependencies and virtual environment
- [x] Configure a database with Docker Compose (PostgreSQL)
- [x] Implement database connection and ORM models
- [x] Define domain model (`User`, `Book`, `ReadingEntry`)
- [x] Build API endpoints for book and reading progress management
- [x] Integrate Supabase OAuth authentication and create auth endpoints
- [x] Add security headers middleware (TrustedHost, GZip)
- [x] Implement dual JWT authentication strategy
- [x] Add comprehensive input validation and business logic

### 🟡 Next steps

- [ ] Set up Alembic and create initial migration
- [ ] Add comprehensive error handling and custom exceptions
- [ ] Implement transaction management for complex operations
- [ ] Add API rate limiting
- [ ] Create health check endpoints
- [ ] Create a Dockerfile for containerized deployment
- [ ] Add CI/CD pipeline configuration
- [ ] Set up monitoring and metrics collection
- [ ] Add backup and recovery procedures
