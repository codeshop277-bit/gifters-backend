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
Sets up SQLAlchemy ORM connection to a PostgreSQL database on AWS RDS and provides database session management utilities.

## Key Components

**Database Connection:**
- Configures PostgreSQL connection via `DATABASE_URL` using AWS RDS credentials
- Creates `engine` (core DB interface) and `SessionLocal` (session factory)

**Core Functions:**
- `init_db()` - Creates all database tables defined in ORM models (inheriting from `Base`)
- `get_db()` - Dependency injection function; yields a DB session and ensures cleanup via try/finally

**ORM Setup:**
- `Base = declarative_base()` - Factory for ORM model base class; all models inherit from this for table mapping

## Security Note
⚠️ **Credentials hardcoded** - DB password and connection details exposed in source code (should use environment variables instead)

---

