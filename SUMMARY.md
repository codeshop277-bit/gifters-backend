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
- [# Database Configuration & Session Management

## Purpose
Sets up SQLAlchemy ORM connection to a PostgreSQL database on AWS RDS and provides utilities for database initialization and session management.

## Key Components

**Database Connection:**
- Configures PostgreSQL connection using AWS RDS credentials (host, port, user, password, database name)
- Creates an `engine` — the core DB interface

**Session Management:**
- `SessionLocal` — factory for creating new database sessions
- `get_db()` — dependency injection function that yields a session and ensures cleanup (closes connection in finally block)

**ORM Setup:**
- `Base` — declarative base class that all ORM models inherit from; enables SQLAlchemy to map Python classes to database tables
- `init_db()` — creates all database tables defined in models by inspecting classes inheriting from `Base`

## Important Functions
- **`init_db()`** — Initialize all tables in the database
- **`get_db()`** — FastAPI dependency for getting a database session with automatic cleanup

**⚠️ Security Note:** Database credentials are hardcoded in source (should use environment variables).](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary: FastAPI Backend Application

**Purpose:** Main entry point for a "Gifters" backend API built with FastAPI.

**Key Logic:**
- Initializes a FastAPI application with CORS middleware to enable cross-origin requests from `localhost:3000`
- CORS is configured to allow credentials, all HTTP methods, and all headers
- Initializes the database via `init_db()`
- Registers route modules for gifts, users, and share functionality

**Important Components:**
- **CORS Middleware**: Allows browser-based requests from the specified frontend origin
- **Route Routers**: Includes endpoints from:
  - `gifts.router` - Gift management
  - `users.router` - User management
  - `share.router` - Sharing functionality
  - `auths.router` - Authentication (currently disabled/commented out)
- **Root Endpoint** (`GET /`): Health check endpoint returning a success message](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
A FastAPI-based REST API for managing gifts and user information with search and filtering capabilities.

## Key Components

**Framework & Validation:**
- FastAPI for HTTP routing
- Pydantic's `BaseModel` for request payload validation (like TypeScript interfaces)
- Type hints for automatic documentation and validation

**Core Endpoints:**

1. **Basic Routes:**
   - `GET /` → Returns greeting message
   - `GET /ping` → Health check endpoint

2. **Path Parameters:**
   - `GET /greet/{name}` → Simple greeting
   - `GET /greet-adv/{name}` → Advanced greeting with optional query params (`excited`, `times`)

3. **Request Body:**
   - `POST /echo` → Echoes text N times using `EchoPayload` schema validation

4. **Query Filtering:**
   - `GET /gifts/search` → Filters mock gift data by `brand` and `max_price` (both optional)
   - `GET /gifts` → Returns all mock gifts

5. **User Endpoints:**
   - `GET /user/{user_id}` → Returns mock user by ID
   - `GET /users/db/{user_id}` → Returns mock user from "database" (incomplete in code)

## Key Logic
- Optional query parameters default to `None`; filtering only applies when provided
- List comprehension for filtering gifts based on multiple conditions
- String comparison is case-insensitive (`lower()`)
- Uses `max()` to prevent invalid repeat counts

**Note:** All data is mocked; no actual database is connected.](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

**Purpose**: SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

**Key Models**:

1. **User** - Core user entity with:
   - Email, hashed password, name
   - Authentication via multiple providers (local, Google, guest)
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Individual gift items with:
   - Details: name, brand, size, color, link, price, note
   - `claimed` flag to track if gift is reserved
   - Foreign key to User (owner)
   - Relationship back to User for ownership tracking

3. **GiftsList** - Gift collection/wishlist with:
   - User ownership via foreign key
   - Unique `share_token` (UUID) for sharing lists with others
   - One-to-many relationship with User

4. **RefreshTokens** - JWT token storage for session management
   - Stores refresh tokens linked to users

5. **ExternalUser** - External authentication data for:
   - Google OAuth integration (stores google_id)
   - Tracks external user metadata separately

6. **AuthProvider (Enum)** - Supported authentication types: local, Google, guest, user

**Key Logic**: Relationship mappings enable bidirectional navigation (e.g., a User can access their `gifts`, and each Gift can reference its `owner`). The `share_token` enables public sharing of gift lists without exposing user IDs.](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Summary

This is a **deployment and configuration guide** for a FastAPI backend application called "gifters-backend", not actual code.

## Key Sections:

1. **Database Migrations** - Uses Alembic to manage schema changes (e.g., adding hashed password column to users table)

2. **AWS RDS Setup** - Instructions to host PostgreSQL/MySQL database on AWS RDS with connection details

3. **AWS EC2 Deployment** - Step-by-step guide to:
   - Launch an EC2 instance
   - Configure security groups (firewall rules) and key pairs
   - SSH into the instance via Git Bash

4. **Server Environment Setup** - Commands to:
   - Install dependencies (Python pip, venv, git, nginx)
   - Clone repository
   - Create isolated Python virtual environment
   - Install project dependencies from `requirements.txt`

5. **Production Service Management** - Create systemd service file to:
   - Run Uvicorn (ASGI server) on port 8000
   - Auto-restart on failure
   - Run as background service 24/7
   - Enable at system startup

## Key Commands:
- `systemctl daemon-reload/start/enable/restart/status fastapi` - Manage the FastAPI service lifecycle

This is essentially a **deployment playbook** for hosting a FastAPI backend on AWS infrastructure.](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# schemas.py Summary

## Purpose
Pydantic validation schemas for a gift-sharing application with user authentication and gift management endpoints.

## Key Components

**User Schemas:**
- `UserCreate` - Registration input (name, email, password)
- `UserLogin` - Login credentials (email, password)
- `UserGuest` - OAuth/social login (email, name, provider_id)
- `UserResponse` - Serialized user output with ORM mode enabled

**Authentication:**
- `GuestResponse` - Returns authenticated user + JWT access token

**Gift Schemas:**
- `GiftTemplate` - Base gift creation schema with optional fields (brand, size, color, link, note, price)
- `GiftResponse` - Full gift output extending template, includes id, user_id, and claimed status with ORM mode
- `GiftOut` - Minimal gift view (id, claimed status, claimed_by user)

## Important Notes
- All response schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to JSON
- Gift price is stored as integer (likely cents/base currency units)
- Supports both traditional auth and OAuth flows (guest signup)](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Marks the containing directory as a Python package, allowing it to be imported as a module
- Currently empty (only contains a comment)
- Serves as an entry point for the package namespace

**Typical Use:** When present, this file enables statements like `from folder_name import module` or `import folder_name.module`.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters"

**Key Components:**
- **FastAPI app instance** - Creates the web server with title "Gifters"
- **Router inclusion** - Registers the `gifts` router from the `routes` module to handle gift-related endpoints

**Function:**
This is a minimal application initialization file that sets up a FastAPI server and connects it to gift management routes defined elsewhere in the codebase.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary

**Purpose:** FastAPI authentication router that sets up Google OAuth2 integration for user login and registration.

**Key Logic:**
- Configures OAuth2 client for Google authentication using credentials from environment variables
- Provides database session dependency injection via `get_db()`
- Includes commented-out OAuth flow implementation

**Important Components:**

1. **OAuth Configuration**: Registers Google as OAuth provider with:
   - Client ID/secret from `.env`
   - Google's OAuth2 endpoints (token, authorize)
   - Requested scopes: openid, email, profile

2. **Commented Endpoints** (disabled):
   - `GET /auth/google/login` - Initiates Google OAuth redirect
   - `GET /auth/google/callback` - Handles OAuth callback:
     - Exchanges authorization code for token
     - Extracts user info (Google ID, email, name)
     - Creates or retrieves `ExternalUser` from database
     - Generates JWT token with user_id, email, role
     - Returns access token to frontend

3. **Database Dependency**: `get_db()` - Manages SQLAlchemy session lifecycle

**Note:** The core OAuth flow is currently commented out, suggesting it's either under development or replaced by alternative authentication method.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Gifts API Router - FastAPI Endpoint Summary

**Purpose:** RESTful API endpoints for managing gift records with user authentication and database operations.

## Key Components:

**Pydantic Models:**
- `GiftCreate` - Request schema for creating gifts (name, brand, size, color)
- `GiftPatch` - Optional fields for partial updates
- `Gift` - Extended GiftCreate with ID
- `GiftResponse` - Response schema from database

**Database & Auth:**
- `get_db()` - Dependency that provides SQLAlchemy session management with automatic cleanup
- JWT token verification via `verify_token()`
- Authorization header validation on protected endpoints

## Endpoints:

1. **GET `/fetch/{user_id}`** 
   - Fetches all gifts for a user
   - Requires `authorization` header with Bearer token
   - Returns `List[GiftResponse]`
   - Validates token before returning results

2. **GET `/searchby/{column}/{value}`**
   - Dynamic column-based search
   - Whitelist validation (id, name, brand, size, color, user_id)
   - Case-insensitive filtering with `func.lower()`
   - Returns matching gift records

3. **POST `/add/{user_id}`** (Incomplete)
   - Creates new gift for user
   - Requires authorization header
   - Uses `GiftTemplate` schema

**Security:** Token-based authentication with JWT verification on sensitive endpoints.](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Summary: Sharable Gift Links API

## Purpose
FastAPI router that enables users to create shareable links to their gift lists and retrieve gifts via those links.

## Key Logic
- **Create shareable link**: Generates a new `GiftsList` record with a unique `share_token` and returns a shareable URL
- **Retrieve gifts by token**: Looks up a `GiftsList` by token, validates it exists, then returns all associated gifts for that user

## Important Functions

| Function | Method | Purpose |
|----------|--------|---------|
| `create_sharable_links()` | POST `/{user_id}` | Creates a sharable gift list link for a user; returns URL with share token |
| `get_gifts()` | GET `/token/{token}` | Retrieves the owner's ID and all their gifts using a share token |

## Notable Details
- Uses SQLAlchemy ORM with automatic dependency injection for database sessions
- Includes error handling for database operations (SQLAlchemyError)
- Returns 401 error if share token is invalid
- Assumes `GiftsList.share_token` is auto-generated (likely UUID)](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# Code Summary

## Purpose
FastAPI router module for user authentication and management endpoints. Handles user registration, login, search, and token-based authorization.

## Key Components

**OAuth2 Security:**
- `oauth2_scheme`: OAuth2PasswordBearer for token validation
- `get_current_user()`: Dependency that validates JWT tokens from request headers, decodes them, and retrieves the authenticated user from database

**Endpoints:**

1. **`/users/search/{id}`** (GET) - Searches for user by ID in database
2. **`/users/post`** (POST) - Creates new user without password hashing (basic endpoint)
3. **`/users/register`** (POST) - User registration with:
   - Email uniqueness validation
   - Password hashing before storage
   - Returns new user object

4. **`/login/basic`** (POST) - Incomplete; appears to be login endpoint

## Key Logic

- **Authentication**: JWT token validation using `jose` library with SECRET_KEY and ALGORITHM
- **Password Security**: Uses `hash_password()` utility to hash passwords before database storage
- **Error Handling**: Returns 401/404 HTTP exceptions for invalid tokens or duplicate emails
- **Database**: SQLAlchemy ORM for User and RefreshTokens model operations

## Important Imports
- FastAPI security modules (OAuth2PasswordBearer)
- JWT handling (jose, verify_token)
- Password utilities (hash_password, verify_password)
- Database models and schemas

**Note**: Code appears incomplete (login endpoint cut off) and has unused commented code.](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Code Summary: Authentication & Password Management Module

## Purpose
This file implements JWT-based authentication and password hashing for a FastAPI application using OAuth2 security scheme.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm
- `verify_password()` - Validates plain password against hashed version
- Uses Passlib's `CryptContext` with automatic deprecation handling for algorithm upgrades

**JWT Authentication:**
- `oauth2_scheme` - Implements OAuth2 Bearer token security (expects token in Authorization header)
- Uses HS256 algorithm with a secret key for token signing/verification

**get_user() Function (Main Logic):**
- FastAPI dependency that extracts and validates JWT tokens from requests
- Decodes JWT payload to retrieve user email (`sub` claim)
- Queries database for matching user record
- Raises `HTTPException(401)` if token is invalid, expired, or user not found
- Returns authenticated `User` object for downstream route handlers

## Security Notes
⚠️ **Warning**: `SECRET_KEY = "protected"` is a hardcoded placeholder—should use environment variables in production.

## Dependencies
- FastAPI security utilities
- Passlib for password hashing
- PyJWT for token operations
- SQLAlchemy ORM for database queries](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles JWT token creation and verification for authentication.

**Key Components:**

1. **Constants:**
   - `SECRET_KEY`: Secret key for signing tokens
   - `ALGORITHM`: HS256 (HMAC SHA-256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Default token lifetime (30 mins)

2. **`create_acces_token()`** - Creates JWT tokens:
   - Accepts data dict and optional expiration delta
   - Sets expiration time (custom or default 30 minutes from now)
   - Returns encoded JWT token signed with secret key

3. **`verify_token()`** - Validates JWT tokens:
   - Decodes token using secret key and algorithm
   - Returns payload if valid
   - Returns `None` on JWTError (invalid/expired tokens)

**Note:** Function has typo: `create_acces_token` should be `create_access_token`. Also, hardcoded `SECRET_KEY` should use environment variables for security.](#\utils\jwthandlerspy)

---


---

