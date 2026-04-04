# gifters-backend Code Summary

**Repository name:** gifters-backend

**Total files analyzed:** 1

---

## Table of Contents

- [\database.py](#\databasepy)

---

## File Summaries

### `\database.py`

# Database Configuration & Session Management

## Purpose
Sets up SQLAlchemy ORM connection to a PostgreSQL database (AWS RDS) and provides utilities for database initialization and session management.

## Key Components

**Database Connection:**
- Connects to AWS RDS PostgreSQL instance using credentials and `create_engine()`
- `SessionLocal` factory creates new ORM sessions for database queries
- `Base` declarative class serves as parent for all ORM models

**Key Functions:**
- `init_db()` - Creates all tables defined in ORM models
- `get_db()` - Dependency injection generator that yields a session and ensures cleanup

**Mock Data:**
- `gifts_mock` - Sample gift items (3 items with id, name, brand, price)
- `users_list` - Sample users (3 users with id, name, email)

## ⚠️ Security Issues
- Database credentials hardcoded (should use environment variables)
- Password exposed in source code
- Credentials visible in DATABASE_URL string

---

