# gifters-backend Code Summary

**Repository name: gifters-backend

**Total files analyzed: 14 

------------

# Table of contents 

- [\database.py](#\databasepy)
- [\main.py](#\mainpy)
- [\mainlearn.py](#\mainlearnpy)
- [\models.py](#\modelspy)
- [\README.md](#\readmemd)
- [\schemas.py](#\schemaspy)
- [\__init__.py](#\initpy)
- [\app\main.py](#\app\mainpy)
- [\routes\auths.py](#\routes\authspy)
- [\routes\gifts.py](#\routes\giftspy)
- [\routes\share.py](#\routes\sharepy)
- [\routes\users.py](#\routes\userspy)
- [\utils\auth.py](#\utils\authpy)
- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)

---

## File summary 

- [\database.py](#\databasepy)
- [# Database Configuration & Initialization

## Purpose
Sets up SQLAlchemy ORM connection to a PostgreSQL database and provides utilities for database session management.

## Key Components

**Database Connection:**
- Creates engine connecting to AWS RDS PostgreSQL instance
- Configures `SessionLocal` factory for creating database sessions

**Core Functions:**
- `init_db()` - Creates all database tables based on ORM models inheriting from `Base`
- `get_db()` - Dependency injection function that yields a session and ensures cleanup (try/finally pattern)

**ORM Setup:**
- `Base` - Declarative base class for all ORM models to inherit from
- `engine` - Core DB interface
- `db` - Active session instance

**Mock Data:**
- `gifts_mock` - Sample gift objects (id, name, brand, price)
- `users_list` - Sample user objects (id, name, email)

## Security Note
⚠️ Database credentials are hardcoded in the file—should be moved to environment variables in production.](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Summary

**Purpose:** Main entry point for a FastAPI backend application called "Gifters" - likely a gift-sharing/management service.

**Key Setup:**
- **CORS Configuration:** Enables cross-origin requests from `localhost:3000` (frontend) with full credential and method support
- **Database:** Initializes database on startup via `init_db()`
- **Routers:** Includes API routes for:
  - `gifts` - gift management
  - `users` - user management
  - `share` - sharing functionality
  - `auths` - authentication (currently disabled)

**Main Component:**
- Single root endpoint (`GET /`) that returns a health check message confirming the backend is running

This is a straightforward FastAPI application setup that serves as the backend API for a gift-sharing platform with modular route organization.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Summary

**Purpose:** A FastAPI REST API for a gift recommendation service ("Gifters API") with mock data endpoints.

## Key Components:

1. **Data Models:**
   - `EchoPayload`: Pydantic schema validating POST request body (text + repeat count)

2. **Core Endpoints:**
   - `GET /` → Health check ("Hello, Gifters!")
   - `GET /ping` → Status endpoint
   - `GET /greet/{name}` → Dynamic greeting
   - `GET /greet-adv/{name}` → Advanced greeting with optional query params (excited, times)
   - `POST /echo` → Echoes/repeats text from payload
   - `GET /gifts` → Returns mock gift list
   - `GET /gifts/search` → Filters gifts by optional brand & max_price parameters
   - `GET /user/{user_id}` → Returns mock user data
   - `GET /users/db/{user_id}` → Returns mock user from list (incomplete)

## Key Logic:
- Path parameters (e.g., `{name}`, `{user_id}`) extract values from URL
- Query parameters (optional) filter results (brand, max_price)
- List comprehension filters mock gift data based on criteria
- FastAPI auto-converts dict returns to JSON responses
- Pydantic validates incoming request bodies against defined schemas

**Status:** Prototype API with hardcoded mock data; no actual database integration.](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
SQLAlchemy ORM model definitions for a gift-sharing application with user authentication and gift list management.

## Key Models

1. **User** - Core user entity
   - Supports multiple auth providers (local, Google, guest)
   - Stores email, hashed password, name, creation timestamp
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Gift items with metadata
   - Properties: name, brand, size, color, price, link, note
   - `claimed` boolean flag tracks if someone claimed the gift
   - Foreign key to User (owner), relationship back to User (claimer)

3. **GiftsList** - Shareable gift lists
   - Links User to their gift lists
   - Auto-generated unique `share_token` (UUID) for sharing lists

4. **RefreshTokens** - JWT token management
   - Stores refresh tokens for users
   - References User via foreign key

5. **ExternalUser** - OAuth user tracking
   - Stores Google OAuth identities separately
   - Tracks email and creation time

## Key Logic
- **Enum constraints**: AuthProvider enum restricts auth methods and user modes to specific values
- **Relationships**: Bidirectional relationships enable navigation (User → Gifts → User, etc.)
- **Timestamps**: Auto-generated UTC timestamps on creation
- **Unique constraints**: Tokens and emails enforce uniqueness at database level](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Gifters-Backend: Deployment & Setup Guide

## Purpose
This is a configuration/deployment documentation file for a **FastAPI backend application** with instructions on database migrations, AWS hosting, and production server setup.

## Key Sections

### 1. **Database Migrations (Alembic)**
- Commands to create and apply database schema changes
- Uses Alembic for version control of database structure
- Example: Adding hashed password column to users table

### 2. **AWS Infrastructure Setup**
- **RDS**: Host PostgreSQL/MySQL database in AWS
- **EC2**: Host the FastAPI backend on AWS virtual machine
  - Configure security groups (firewall rules for inbound/outbound traffic)
  - Generate SSH key pairs for secure connection

### 3. **EC2 Instance Configuration**
- SSH connection to Ubuntu instance
- Install dependencies: Python, pip, venv, git, Nginx
- Clone repository and set up isolated Python environment

### 4. **Application Deployment**
- Create Python virtual environment
- Install dependencies from `requirements.txt`
- Run Uvicorn development server (FastAPI ASGI server)

### 5. **Production Service Setup (Systemd)**
- Creates a systemd service file to run Uvicorn 24/7
- **Key settings:**
  - Auto-restart on failure
  - Runs as ubuntu user
  - Binds to port 8000
  - Sets Python unbuffered output for logging
- Commands to manage service (start, enable, restart, check status)

## Summary
Complete guide for deploying a FastAPI application on AWS with persistent database and always-on backend service.](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Pydantic Schemas Summary

**Purpose:** Defines request/response validation schemas for a gift-sharing API with user authentication and guest access.

## Key Components:

**User Schemas:**
- `UserCreate` - Registration (name, email, password)
- `UserLogin` - Login credentials (email, password)
- `UserGuest` - OAuth/social login (email, name, provider_id)
- `UserResponse` - Serialized user output (id, name, email) with ORM mode enabled

**Authentication:**
- `GuestResponse` - Returns user data + JWT access token for logged-in guests

**Gift Schemas:**
- `GiftTemplate` - Core gift fields (name, brand, size, color, link, note, price)
- `GiftResponse` - Full gift object with metadata (id, user_id, claimed status, ORM compatible)
- `GiftOut` - Minimal gift view (id, claimed status, claimed_by name)

**Key Feature:** All response models use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to Pydantic models. Optional fields allow flexible gift creation and updates.](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Details:**
- Marks the containing directory as a Python package, making it importable
- Currently empty (or minimal) - no custom initialization logic is defined
- Allows other modules to import from this package using `from package_name import ...`

This is a standard convention in Python projects with no functional code at this time.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters"

**Key Components:**
- Creates a FastAPI instance with the title "Gifters"
- Includes the gifts router from the `routes.gifts` module to handle gift-related API endpoints

**Functionality:** Serves as the application bootstrap that sets up the API server and registers route handlers for gift operations.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary: Google OAuth Authentication Module

## Purpose
FastAPI authentication router that implements Google OAuth2 login flow with JWT token generation for external users.

## Key Components

1. **OAuth Configuration**: Registers Google OAuth app with credentials from environment variables (client ID/secret, Google endpoints)

2. **Database Dependency**: `get_db()` function provides SQLAlchemy session management with cleanup

3. **Commented-Out Endpoints** (currently disabled):
   - **`/google/login`**: Initiates Google OAuth redirect
   - **`/google/callback`**: Handles OAuth callback, which:
     - Extracts user info (Google ID, email, name) from OAuth token
     - Creates new `ExternalUser` in database or retrieves existing user
     - Generates JWT token with user_id, email, and "external" role
     - Returns access token to frontend

## Important Logic
- **User lookup/creation**: Checks if Google ID exists; creates record only if new
- **JWT generation**: Encodes payload with user info using HS256 algorithm and secret from env

## Status
Code is currently commented out, likely pending frontend integration or further development.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary: FastAPI Gifts Management Router

## Purpose
This file defines API endpoints for managing gift records in a FastAPI application. It handles gift creation, retrieval, and search operations with JWT-based authentication.

## Key Components

### Pydantic Models (Data Validation)
- **GiftCreate**: Input schema for new gifts (name, brand, size, color)
- **GiftPatch**: Partial update schema (all fields optional)
- **GiftResponse**: Response schema for gift data
- **Gift**: Combines GiftCreate with an ID field

### Database
- `get_db()`: Dependency function that provides database session management with proper cleanup (try/finally pattern)

### API Endpoints

1. **`GET /gifts/fetch/{user_id}`**
   - Retrieves all gifts for a specific user
   - Requires JWT token in Authorization header
   - Returns list of GiftResponse objects
   - Validates token before returning data

2. **`GET /gifts/searchby/{column}/{value}`**
   - Searches gifts by any allowed column (id, name, brand, size, color, user_id)
   - Case-insensitive search with whitespace trimming
   - Uses SQLAlchemy's dynamic column attribute retrieval (`getattr`)
   - Returns 404 if column invalid or no results found

3. **`POST /gifts/add/{user_id}`** (incomplete in snippet)
   - Creates new gift for a user
   - Requires authorization header

## Key Logic
- **Authentication**: JWT token validation via Authorization header
- **Query Building**: Uses SQLAlchemy ORM with dynamic column filtering
- **Error Handling**: HTTPException responses for missing data, invalid tokens, and bad requests](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Code Summary

**Purpose:** FastAPI router for creating and retrieving shareable gift list links.

**Key Logic:**
- Generates unique shareable tokens for gift lists, allowing users to share their wishlists via URLs
- Retrieves gifts associated with a shared list using token-based authentication

**Key Functions:**

1. **`create_sharable_links(user_id)`** - POST endpoint
   - Creates a new `GiftsList` record for a user
   - Returns a shareable URL containing an auto-generated `share_token`
   - Handles database errors with rollback and HTTP 500 response

2. **`get_gifts(token)`** - GET endpoint
   - Retrieves a gift list by its `share_token`
   - Fetches all gifts belonging to the list owner
   - Returns owner ID and associated gifts
   - Raises HTTP 401 if token is invalid

**Note:** The code assumes `share_token` is auto-generated in the `GiftsList` model (likely using UUID). Debug print statements are present for development.](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# User Management API Router

## Purpose
FastAPI router handling user authentication and management endpoints with JWT token-based security.

## Key Components

**Authentication:**
- `get_current_user()` - Dependency that validates JWT tokens from request headers, decodes payload, retrieves user from DB, returns authenticated user or raises 401 exception

**Endpoints:**
- `GET /users/search/{id}` - Fetch user by ID
- `POST /users/post` - Create new user (no validation)
- `POST /users/register` - User registration with password hashing and duplicate email check
- `POST /users/login/basic` - Login endpoint (incomplete)

## Key Logic
1. **Registration** - Validates email uniqueness, hashes password using `hash_password()`, stores both plain and hashed passwords in DB
2. **Token Security** - Uses OAuth2 Bearer scheme with JWT (HS256), extracts user_id from token claims
3. **Database** - SQLAlchemy ORM queries against User and RefreshTokens models

## Notes
- Code is incomplete (login endpoint cuts off)
- Potential security issue: stores both plain and hashed passwords
- Commented code suggests refactoring in progress
- Mixed patterns: some endpoints validate input, others don't](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Summary: Authentication & Security Module

## Purpose
Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256
- `verify_password()` - Compares plain text password against hashed version

**Token & Security Setup:**
- `OAuth2PasswordBearer` - Defines token extraction from requests (expects "Authorization: Bearer {token}")
- `SECRET_KEY` & `ALGORITHM` - JWT signing credentials (HS256)
- `pwd_context` - Passlib context for secure password operations with auto-deprecation of old schemes

**User Authentication:**
- `get_user()` - Dependency function that:
  1. Extracts JWT token from request header
  2. Decodes token using SECRET_KEY and validates signature
  3. Extracts email (`sub` claim) from payload
  4. Queries database for matching user
  5. Returns user or raises 401 Unauthorized exception

## Important Notes
⚠️ **Security Issue**: `SECRET_KEY = "protected"` is hardcoded and weak—should use environment variables with strong secrets in production.](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles JWT authentication token creation and verification for securing API endpoints.

**Key Logic:**
- Creates signed JWT tokens with configurable expiration (default 30 minutes)
- Verifies token validity by decoding and catching JWT errors
- Uses HS256 symmetric encryption with a secret key

**Important Functions:**

1. **`create_acces_token()`** - Generates JWT token
   - Copies input data, adds expiration timestamp
   - Encodes with secret key and HS256 algorithm
   - Accepts custom expiration delta or uses default 30 minutes

2. **`verify_token()`** - Validates JWT token
   - Decodes token using secret key
   - Returns payload if valid, `None` if expired/invalid

**Note:** Contains a hardcoded secret key (security risk in production) and a typo in function name (`acces_token`).](#\utils\jwthandlerspy)

---


---

