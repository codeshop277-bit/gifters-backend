# gifters-backend Code Summary

**Repository name:** gifters-backend

**Total files analyzed:** 1

---

## Table of Contents

- [\database.py](#\databasepy)

---

## File Summaries

### `\database.py`

# Database Configuration Summary

**Purpose:** Establishes SQLAlchemy ORM setup and PostgreSQL database connection for a gift management application.

**Key Components:**

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance (`gifters.cx8wyeoaoo49.eu-north-1.rds.amazonaws.com`)
   - Creates engine as the core DB interface

2. **Session Management**
   - `SessionLocal`: Factory for creating database sessions
   - `db`: Active session instance for DB operations
   - `get_db()`: Generator function that yields sessions and ensures cleanup (used as FastAPI dependency for request isolation)

3. **ORM Base**
   - `Base`: Declarative base class for all SQLAlchemy models to inherit from
   - `init_db()`: Creates all tables defined in models during app startup

**Important Functions:**
- `init_db()`: Initialize database schema
- `get_db()`: Dependency injection pattern for per-request database sessions

**Note:** Credentials are hardcoded (security risk—should use environment variables).

---

