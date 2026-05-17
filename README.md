# Intelligent Journaler
Intellient Journaler is a REST API used for managing and filtering journal entries. Its key feature is an AI engine that generates insights based on the entry content.

First, you need to register and sign in; then, you can create, read, update, and delete your entries. It also allows you to filter your entries by date and tags.

## Features

- Entry management
- JWT Authorization
- Filtering by tags and date
- AI generated insights

## Installation

### 1. Clone the repository

- git clone https://github.com/Kelooo0/intelligent-journaler.git
- cd intelligent-journaler

### 2. Create .env file

- Using .env.example file create .env file
- Change SECRET_KEY to a safe and long string of characters
- Set API_KEY to your gemini api key created at: https://aistudio.google.com/


### 3. Run the application

1. First download and run docker desktop app
2. Make sure you docker Docker Desktop app is running
3. Choose one of the options below to run in your designated terminal
3. Development Variant: docker compose up --build
4. Production Variant: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
5. After running the app go to localhost:8000/docs on dev variant or localhost:80/docs on prod variant
6. Then after you register and sign in you can test all endpoints using swagger

## Project structure

```text
intelligent-journaler/
├── alembic/                    # Migrations folder
├── app/                        # Main app package
│   ├── routers/                # FastAPI routers
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   └── entries.py          # Entries endpoints
│   ├── services/
│   │   ├── ai_service.py       # AI insights generating service
│   │   ├── auth_service.py     # Service for registering and signing in user
│   │   ├── entries_service.py  # Service for entries CRUD
│   │   └── tags_service.py     # Service for operations on tags
│   ├── __init__.py
│   ├── config.py               # All app settings
│   ├── database.py             # Database configuration file
│   ├── main.py                 # App initialization file
│   ├── models.py               # Database models file
│   └── schemas.py              # Pydantic data schemas
├── tests/
│   ├── conftest.py             # File for pytest fixtures
│   ├── test_auth.py            # Authentication tests
│   └── test_entries.py         # Entries tests
├── .env                        # Sensitive settings
├── .env.example                # Example settings for .env
├── .gitignore                  # Files to ignore for git
├── alembic.ini
├── docker-compose.override.yml # Docker compose file for development use
├── docker-compose.prod.yml     # Docker compose file for production use
├── docker-compose.yml          # Base docker compose settings
├── Dockerfile                  # Docker image building settings
├── pyproject.toml              # Additional pytest settings
├── README.md
└── requirements.txt            # Application dependencies
