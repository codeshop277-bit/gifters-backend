# gifters-backend Code Summary

**Repository name:** gifters-backend

**Total files analyzed:** 14

---

## Table of Contents

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

## File Summaries

### `\database.py`

# Code Summary

## Purpose
Database configuration and initialization file for a FastAPI gift-tracking application connecting to AWS RDS PostgreSQL database.

## Key Components

**Database Connection Setup:**
- Configures PostgreSQL connection to AWS RDS instance with credentials (host, port, user, password, database name)
- Creates SQLAlchemy `engine` for database I/O and `SessionLocal` factory for creating database sessions

**Core Functions:**
- `init_db()` - Creates all database tables based on ORM models inheriting from `Base`
- `get_db()` - Generator function that yields a database session for dependency injection in API endpoints, ensuring proper cleanup with `finally` block

**ORM Base:**
- `Base = declarative_base()` - Factory that creates base class for all SQLAlchemy models; enables automatic table mapping

**Mock Data:**
- `gifts_mock` - Sample gift items with id, name, brand, price
- `users_list` - Sample user profiles with id, name, email

## Important Notes
⚠️ **Security Issue**: Database credentials hardcoded in source code (should use environment variables)

---

### `\main.py`

# Code Summary

**Purpose:** Main entry point for a FastAPI backend application called "Gifters" - likely a gift management/sharing platform.

**Key Components:**

1. **CORS Configuration** - Enables cross-origin requests from `http://localhost:3000` (frontend), allowing credentials and all HTTP methods/headers

2. **Database Initialization** - Calls `init_db()` to set up the database on startup

3. **Route Registration** - Includes routers for:
   - `gifts` - Gift management endpoints
   - `users` - User management endpoints
   - `share` - Sharing functionality endpoints
   - `auths` - Authentication (currently disabled/commented out)

4. **Health Check Endpoint** - Simple GET `/` route returning a success message

**Core Logic:** Standard FastAPI application setup with middleware configuration for frontend communication and modular route organization.

---

### `\mainlearn.py`

# Code Summary: Gifters API (FastAPI)

## Purpose
A simple REST API built with FastAPI for managing gifts and user data. Serves as a learning/demo project with mock data and basic CRUD operations.

## Key Components

### Data Models
- **EchoPayload**: Pydantic schema validating POST request body with `text` (required) and `repeat` (optional, default=1)

### Core Endpoints

**Basic Routes:**
- `GET /` - Health check, returns greeting
- `GET /ping` - Status endpoint

**Echo/Transform:**
- `POST /echo` - Repeats text N times based on payload

**Gifts:**
- `GET /gifts` - Returns mock gift list
- `GET /gifts/search` - Filters gifts by optional `brand` and `max_price` query params (case-insensitive matching)

**Users:**
- `GET /user/{user_id}` - Returns mock user by ID
- `GET /users/db/{user_id}` - Returns mock user from "database"

**Parameterized Routes:**
- `GET /greet/{name}` - Path parameter greeting
- `GET /greet-adv/{name}` - Advanced greeting with optional `excited` (bool) and `times` (int) query params

## Important Patterns
- Uses FastAPI decorators (`@app.get`, `@app.post`) to route requests
- Path parameters: `{name}`, `{user_id}`
- Query parameters: `?brand=Nike&max_price=50`
- Optional types for nullable query params
- Automatic JSON serialization of returned dicts
- List comprehension for filtering (gifts search)

**Note:** Code appears incomplete (users endpoint

---

### `\models.py`

# Code Summary

**Purpose:** SQLAlchemy ORM models for a gift management application with user authentication and sharing features.

**Key Models:**

1. **User** - Core user entity with:
   - Authentication support (local, Google OAuth, guest)
   - Email, hashed password, name fields
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Gift items with:
   - Details: name, brand, size, color, price, link, note
   - `claimed` boolean flag to track if gift is claimed
   - Foreign key to User (owner)
   - Bidirectional relationship back to User

3. **GiftsList** - Shareable gift list container:
   - Unique `share_token` (UUID) for public sharing
   - Linked to User via foreign key
   - Tracks creation timestamp

4. **RefreshTokens** - JWT token management:
   - Stores refresh tokens per user for session persistence

5. **ExternalUser** - OAuth integration:
   - Tracks Google OAuth users separately with `google_id`

**Key Logic:**
- `AuthProvider` enum restricts authentication methods to: local, Google, guest, user
- Relationships use `back_populates` to enable bidirectional navigation (User ↔ Gifts)
- UUID auto-generation for gift list sharing tokens
- Timestamp defaults for audit trails

---

### `\README.md`

# Summary: gifters-backend Deployment & Setup Guide

## Purpose
This is a **deployment and infrastructure setup guide** for a FastAPI backend application. It covers database migrations, AWS hosting (RDS + EC2), and production server configuration.

## Key Sections

### 1. **Database Migrations (Alembic)**
- Add/modify database columns using Alembic's auto-generate feature
- Commands: `alembic revision`, `alembic upgrade head`

### 2. **AWS RDS Setup**
- Host PostgreSQL/MySQL database in AWS RDS
- Retrieve connection credentials (host, port, etc.) for backend configuration

### 3. **AWS EC2 Instance Setup**
- Launch Linux instance with security groups and key pair authentication
- Install dependencies: Python3, pip, venv, git, nginx

### 4. **Application Deployment**
- Clone repo → create virtual environment → install requirements
- Run Uvicorn server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 5. **Production Service Configuration**
- Create systemd service file (`/etc/systemd/system/fastapi.service`)
- Configure auto-restart and persistent running
- Commands: `systemctl start/enable/restart/status fastapi`

## Important Components
- **Security Groups**: Control inbound/outbound network traffic
- **Systemd Service**: Ensures 24/7 uptime with auto-restart on failure
- **Virtual Environment**: Isolates project dependencies
- **Nginx**: Production web server (referenced but not configured in detail)

---

### `\schemas.py`

# Summary: Pydantic Schemas for User & Gift Management API

## Purpose
Defines request/response validation schemas for a gift registry application with user authentication (including guest login) and gift management.

## Key Components

**User Schemas:**
- `UserCreate` - Registration payload (name, email, password)
- `UserLogin` - Login payload (email, password)
- `UserGuest` - Social/guest login payload (email, name, provider_id)
- `UserResponse` - API response with user data (id, name, email); uses `orm_mode` for SQLAlchemy compatibility

**Authentication:**
- `GuestResponse` - Login response wrapping user data + JWT access token

**Gift Schemas:**
- `GiftTemplate` - Base gift attributes (name, brand, size, color, link, note, price)
- `GiftResponse` - Full gift data extending template with id, user_id, claimed status; uses `orm_mode`
- `GiftOut` - Minimal gift response for list views (id, claimed status, claimed_by user)

## Key Features
- All response schemas enable `orm_mode=True` for direct SQLAlchemy ORM object serialization
- Optional fields for flexible gift metadata
- Inheritance pattern (`GiftResponse` extends `GiftTemplate`) to reduce duplication

---

### `\__init__.py`

# Summary

**Purpose:** This is an `__init__.py` file, which serves as a Python package marker.

**Key Points:**
- The file is empty (or nearly empty) with only a comment
- Its presence in a folder tells Python to treat that folder as a package/module
- Allows the folder's contents to be imported using standard Python import statements
- Enables the folder structure to be recognized as part of the package hierarchy

**Functionality:** No active logic—purely declarative by existence.

---

### `\app\main.py`

# Code Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters" that manages gift-related functionality.

**Key Logic:**
- Creates a FastAPI application instance with the title "Gifters"
- Registers routes from the `gifts` module using `include_router()`

**Components:**
- `FastAPI()` - Initializes the web application
- `gifts.router` - Router object imported from `routes/gifts.py` that contains all gift-related endpoints

This is a minimal application setup that delegates all API endpoints to the gifts router module.

---

### `\routes\auths.py`

# Summary

**Purpose:** FastAPI authentication module that sets up Google OAuth 2.0 integration for user login and registration.

**Key Logic:**
- Registers Google OAuth client with credentials from environment variables
- Configures OAuth flow endpoints (authorization and token URLs)
- Provides database session dependency injection

**Important Components:**

1. **OAuth Configuration** - Sets up Google OAuth with client ID/secret and scopes (openid, email, profile)

2. **`get_db()`** - Dependency function that yields a database session and ensures cleanup

3. **Commented-out Endpoints:**
   - `/google/login` - Redirects to Google's OAuth authorization page
   - `/google/callback` - Handles OAuth callback to:
     - Exchange authorization code for access token
     - Extract user info (Google ID, email, name)
     - Create or retrieve `ExternalUser` from database
     - Generate JWT token with user_id, email, and role
     - Return access token to frontend

**Status:** OAuth callback logic is currently disabled (commented out), suggesting the module is under development or awaiting frontend integration.

---

### `\routes\gifts.py`

# Summary

**Purpose:** FastAPI router for managing gift records - enables users to fetch, search, and add gifts with JWT authentication.

## Key Components:

**Pydantic Models:**
- `GiftCreate`, `Gift`, `GiftPatch` - request/response schemas for gift data validation
- `GiftDataBase` - wraps list of gifts

**Database Layer:**
- `get_db()` - dependency that provides SQLAlchemy Session with proper cleanup

**Endpoints:**

1. **GET `/fetch/{user_id}`** - Retrieves all gifts for a user
   - Validates JWT token from Authorization header
   - Queries `Gifts` table filtered by user_id
   - Returns `List[GiftResponse]`

2. **GET `/searchby/{column}/{value}`** - Searches gifts by column
   - Whitelist validates allowed columns (id, name, brand, size, color, user_id)
   - Uses `getattr()` for dynamic column attribute access
   - Case-insensitive search with whitespace trimming

3. **POST `/add/{user_id}`** - Creates new gift (incomplete in snippet)
   - Takes `GiftTemplate` and user_id
   - Validates authorization header

**Key Logic:**
- JWT token verification via Authorization header (`Bearer <token>`)
- Dynamic SQL filtering using SQLAlchemy's `func.lower()` for case-insensitive queries
- Error handling with 401/404 HTTP exceptions
- Database dependency injection pattern

---

### `\routes\share.py`

# Summary: Sharable Gift Links API

**Purpose:** FastAPI router that creates and retrieves shareable gift lists via unique tokens.

**Key Logic:**
- Generates unique share URLs for users to distribute their gift lists
- Validates tokens and retrieves associated gifts without requiring authentication

**Main Endpoints:**

1. **`POST /{user_id}`** - Create sharable link
   - Creates a new `GiftsList` entry for the user
   - Generates a unique `share_token` (auto-generated by model)
   - Returns shareable URL: `http://localhost:3000/share/{share_token}`
   - Includes error handling with rollback on database failures

2. **`GET /token/{token}`** - Retrieve gifts by token
   - Validates the share token exists
   - Fetches all gifts belonging to the list owner
   - Returns owner ID and gift list
   - Raises 401 error if token is invalid

**Dependencies:**
- FastAPI, SQLAlchemy ORM, UUID handling
- Database models: `GiftsList`, `Gifts`

---

### `\routes\users.py`

# User Authentication & Management API Router

## Purpose
FastAPI router for user authentication and management, handling user registration, login, and protected endpoints with JWT token-based authentication.

## Key Components

### Authentication
- **`get_current_user()`**: Dependency that validates JWT tokens from request headers, decodes them, and retrieves the authenticated user from the database. Raises 401 error for invalid/expired tokens.
- **`oauth2_scheme`**: OAuth2 password bearer scheme for token extraction from Authorization headers.

### Endpoints

1. **`GET /users/search/{id}`** - Searches for a user by ID, returns 404 if not found

2. **`POST /users/post`** - Creates a new user from `UserCreate` schema data

3. **`POST /users/register`** - User registration with:
   - Duplicate email validation
   - Password hashing via `hash_password()`
   - Stores both plain and hashed passwords in DB

4. **`POST /users/login/basic`** - *(incomplete in snippet)* Likely handles basic login with credentials

## Dependencies
- SQLAlchemy ORM for database queries
- JWT (via `jose`) for token creation/verification
- Password hashing utilities
- Pydantic schemas for request/response validation

## Issues
- Incomplete `/login/basic` endpoint
- Storing both plain and hashed passwords (security risk)
- Mixed use of `users_list` and database queries

---

### `\utils\auth.py`

# Security & Authentication Module Summary

**Purpose:** Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

**Key Components:**

1. **Password Management:**
   - `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm
   - `verify_password()` - Compares plain text password against hashed version

2. **JWT Authentication:**
   - `oauth2_scheme` - OAuth2 flow that expects Bearer tokens in request headers
   - `get_user()` - Dependency function that:
     - Extracts JWT token from request
     - Decodes token using HS256 algorithm and SECRET_KEY
     - Retrieves user email ("sub" claim) from token payload
     - Queries database to fetch User object by email
     - Returns authenticated user or raises 401 HTTPException on failure

**Key Logic:**
- Uses passlib's CryptContext for secure password hashing with auto-deprecation of older schemes
- Implements standard OAuth2 Bearer token flow
- JWT validation includes error handling for malformed tokens and missing users
- Returns HTTPException (401) if token is invalid or user doesn't exist

**Note:** `SECRET_KEY = "protected"` is a hardcoded placeholder—should use environment variables in production.

---

### `\utils\jwt_handlers.py`

# JWT Token Management Module

**Purpose:** Handles JWT (JSON Web Token) creation and verification for user authentication/authorization.

**Key Components:**

- **Constants:**
  - `SECRET_KEY`: Signing key for JWT tokens (hardcoded, should use environment variables)
  - `ALGORITHM`: HS256 for symmetric encryption
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Default token TTL of 30 minutes

- **`create_acces_token(data, expires_delta)`**: 
  - Creates signed JWT tokens
  - Accepts custom expiration time or uses 30-minute default
  - Adds `exp` claim with expiration timestamp
  - Returns encoded JWT string

- **`verify_token(token)`**: 
  - Decodes and validates JWT signature using the secret key
  - Returns payload dict if valid, `None` if verification fails (expired, invalid signature, etc.)

**Note:** This is a basic implementation. Production use should store `SECRET_KEY` in environment variables and use HTTPS.

---

