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

**Purpose:** Sets up SQLAlchemy ORM connection to a PostgreSQL database on AWS RDS.

**Key Components:**

1. **Connection Setup**
   - Creates database engine connecting to AWS RDS instance (`gifters.cx8wyeoaoo49.eu-north-1.rds.amazonaws.com`)
   - Credentials hardcoded in variables (DB_HOST, DB_USER, DB_PASSWORD, etc.)

2. **Session Factory**
   - `SessionLocal`: Factory for creating database sessions
   - `db`: Single session instance for DB operations

3. **ORM Base**
   - `Base`: Declarative base class that all model classes inherit from

4. **Key Functions**
   - `init_db()`: Creates all database tables defined in models
   - `get_db()`: Dependency injection function yielding a session and ensuring cleanup

**Important Note:** Database credentials are hardcoded in source code (security risk—should use environment variables).

---

