# gifters-backend Code Summary

**Repository name:** gifters-backend

**Total files analyzed:** 1

---

## Table of Contents

- [\database.py](#\databasepy)

---

## File Summaries

### `\database.py`

# Database Configuration & Initialization

**Purpose:** Sets up SQLAlchemy ORM connection to a PostgreSQL database and provides utilities for database session management.

**Key Components:**

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance using credentials and creates an engine
   - `DATABASE_URL`: PostgreSQL connection string

2. **Session Factory**
   - `SessionLocal`: Factory for creating database sessions with `autocommit=False` and `autoflush=False`
   - `db`: Initial session instance

3. **ORM Base**
   - `Base = declarative_base()`: Base class for all SQLAlchemy ORM models to inherit from

4. **Key Functions**
   - `init_db()`: Creates all database tables defined in ORM models (called on app startup)
   - `get_db()`: Dependency injection generator that yields a session and ensures cleanup via `finally` block

**Important Notes:**
- ⚠️ **Security issue**: Database credentials are hardcoded (should use environment variables)
- The commented code at bottom shows example Pydantic models (GiftCreate, Gift) for API schemas
- Designed for FastAPI dependency injection pattern via `get_db()`

---

