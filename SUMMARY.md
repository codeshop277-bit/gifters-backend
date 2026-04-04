# gifters-backend Code Summary

**Repository name:** gifters-backend

**Total files analyzed:** 1

---

## Table of Contents

- [\database.py](#\databasepy)

---

## File Summaries

### `\database.py`

# Database Configuration & Setup

**Purpose:** Establishes PostgreSQL database connection and session management for a gift-tracking application.

## Key Components:

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance using SQLAlchemy engine
   - Credentials hardcoded (security risk - should use environment variables)

2. **Session Management**
   - `SessionLocal`: Factory for creating database sessions
   - `get_db()`: Dependency injection function that yields sessions and ensures cleanup

3. **ORM Base Setup**
   - `Base`: Declarative base class for all SQLAlchemy models to inherit from
   - `init_db()`: Creates all tables based on defined models in the database

4. **Mock Data**
   - `gifts_mock`: Sample gift objects (id, name, brand, price)
   - `users_list`: Sample user objects (id, name, email)

## Important Functions:
- `get_db()` - FastAPI dependency for providing DB sessions to endpoints
- `init_db()` - Initializes database schema on application startup

**Note:** Database credentials are exposed in source code—should be moved to environment variables for production.

---

