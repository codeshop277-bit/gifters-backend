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
- [# Code Summary

## Purpose
Database initialization and configuration for a FastAPI/SQLAlchemy application connected to an AWS PostgreSQL database.

## Key Components

**Database Connection:**
- Establishes connection to AWS RDS PostgreSQL instance using credentials (⚠️ hardcoded—security risk)
- Creates engine and sessionmaker for database operations

**Core Objects:**
- `engine`: Database connection interface
- `SessionLocal`: Factory for creating DB sessions
- `Base`: Declarative base class for ORM models to inherit from

**Key Functions:**
- `init_db()`: Creates all database tables defined in models
- `get_db()`: Generator that provides a DB session to API endpoints (with automatic cleanup via try/finally)

**Mock Data:**
- `gifts_mock`: Sample gift items (Shirt, Cap, Shoes with brand/price)
- `users_list`: Sample user records (Alice, Bob, Charlie with email)

## Notes
- Mock data suggests this is for a gift/wishlist application
- Commented-out code shows Pydantic models for gift creation/validation
- **Security issue**: Database credentials hardcoded in source code](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI backend application called "Gifters" - a gift management system.

**Key Logic:**
- **CORS Configuration:** Enables cross-origin requests from `localhost:3000` (frontend) with credentials and all HTTP methods/headers allowed
- **Database Initialization:** Calls `init_db()` to set up the database
- **Route Registration:** Registers routers for gifts, users, and share functionality (auth router is commented out)

**Important Components:**
- `FastAPI(title="Gifters")` - Creates the main application instance
- `CORSMiddleware` - Handles cross-origin request validation
- Route routers included: `gifts`, `users`, `share`
- `@app.get("/")` - Health check endpoint returning a success message

**Tech Stack:** FastAPI with CORS support for browser-based requests.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
A FastAPI-based REST API for a gift shopping application with endpoints for greeting users, searching/listing gifts, and retrieving user information.

## Key Components

**Data Model:**
- `EchoPayload` - Pydantic schema validating POST body with `text` (required) and `repeat` (optional, default=1)

**Core Endpoints:**

1. **Utility Routes:**
   - `GET /` - Root endpoint returning greeting
   - `GET /ping` - Health check

2. **Greeting Routes:**
   - `GET /greet/{name}` - Simple greeting with path parameter
   - `GET /greet-adv/{name}` - Advanced greeting with optional query params (`excited`, `times`)

3. **Echo Route:**
   - `POST /echo` - Repeats text based on `EchoPayload` (validates request body)

4. **Gifts Routes:**
   - `GET /gifts` - Returns hardcoded gift list
   - `GET /gifts/search` - Filters gifts by optional `brand` and `max_price` query parameters (case-insensitive brand matching)

5. **User Routes:**
   - `GET /user/{user_id}` - Returns mock user by ID
   - `GET /users/db/{user_id}` - Partially implemented; retrieves from mock users list (code appears truncated)

## Key Logic
- Uses **path parameters** (`{name}`, `{user_id}`) for dynamic routing
- Uses **query parameters** (optional filters) with `Optional[T]` type hints
- **Filtering logic** in `/gifts/search` uses list comprehension with conditional matching
- All responses auto](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models

**User**
- Core user entity with email, hashed password, name
- Supports multiple auth providers (local, Google, guest)
- One-to-many relationship with Gifts and GiftsList

**Gifts**
- Gift items with details (name, brand, size, color, price, link, note)
- Has `claimed` boolean flag to track if someone claimed it
- Foreign key to User (owner), with back-populate relationship for easy access

**GiftsList**
- Represents a shareable gift list/wishlist
- Linked to User with unique share_token (UUID) for sharing purposes
- Tracks creation timestamp

**RefreshTokens**
- Stores JWT refresh tokens per user for session management

**ExternalUser**
- Tracks Google OAuth users separately (google_id, email, name)

**AuthProvider Enum**
- Defines supported authentication methods: `local`, `google`, `guest`, `user`

## Key Features
- Bidirectional relationships (back_populates) for convenient data access
- UUID-based shareable gift list tokens
- UTC timezone-aware timestamps
- Foreign key constraints ensuring referential integrity
- Support for social login and traditional authentication](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Summary: Gifters Backend Deployment Guide

## Purpose
This is a **deployment and setup guide** for a FastAPI backend application, covering database migrations, AWS hosting (RDS + EC2), and production service management.

## Key Sections

### 1. **Database Migrations (Alembic)**
- Commands for auto-generating migration scripts
- Applies schema changes to existing tables (e.g., adding hashed password column)

### 2. **AWS Infrastructure Setup**
- **RDS**: Hosts the PostgreSQL/MySQL database
- **EC2**: Hosts the backend application on Ubuntu instance
- **Security Configuration**: Key pairs (SSH authentication) and security groups (firewall rules for inbound/outbound traffic)

### 3. **EC2 Instance Setup**
- Install dependencies: Python3, pip, venv, git, nginx
- Clone repository and create isolated Python virtual environment
- Install project dependencies via `requirements.txt`
- Run Uvicorn development server on port 8000

### 4. **Production Service Management**
- **Systemd service file** (`fastapi.service`) automatically runs Uvicorn 24/7
- Key configurations:
  - Auto-restart on failure (`Restart=always`)
  - Runs as `ubuntu` user
  - Working directory: `/home/ubuntu/gifters_backend`
  - Environment variables for Python buffering

### Important Commands
```bash
systemctl daemon-reload    # Reload service configs
systemctl start/stop/restart fastapi
systemctl enable fastapi   # Auto-start on reboot
systemctl status fastapi   # Check service health
```

**Result**: Production-ready FastAPI backend running continuously on EC2 with automated service management.](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Code Summary: Pydantic Schemas

**Purpose:** Defines data validation and serialization schemas for API requests/responses using Pydantic.

**Key Components:**

1. **User Schemas**
   - `UserCreate`: Registration payload (name, email, password)
   - `UserLogin`: Login payload (email, password)
   - `UserGuest`: OAuth guest user (email, name, provider_id)
   - `UserResponse`: API response model with ORM mode for SQLAlchemy compatibility

2. **Gift Management Schemas**
   - `GiftTemplate`: Base gift creation model with optional fields (brand, size, color, link, note, price)
   - `GiftResponse`: Extends template with database fields (id, user_id, claimed status)
   - `GiftOut`: Minimal gift response (id, claimed status, claimed_by user name)

3. **Authentication Response**
   - `GuestResponse`: Combines user data with JWT access token

**Important Detail:** All response schemas use `orm_mode = True` to automatically convert SQLAlchemy ORM objects to JSON-serializable Pydantic models.](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is an `__init__.py` file, which marks the containing folder as a Python package.

**Key Points:**
- Empty or minimal initialization file
- Enables the folder to be imported as a Python module
- Allows other Python files to import modules/components from this package using `from package_name import ...`

No significant logic or functions present in this file.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters"

**Key Logic:**
- Creates a FastAPI application instance with the title "Gifters"
- Registers the gifts router to handle gift-related API endpoints

**Components:**
- `app`: FastAPI application object that serves as the core server
- `gifts.router`: Router module imported from `routes/gifts.py` that contains gift-related API routes

This is a minimal setup file that initializes the web service and connects it to its routing logic.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary: Google OAuth Authentication Module

## Purpose
FastAPI authentication router that implements Google OAuth 2.0 login flow for external users.

## Key Components

**OAuth Setup:**
- Registers Google OAuth client with credentials from environment variables
- Configured endpoints for token exchange and authorization

**Database:**
- `get_db()` - Dependency function providing SQLAlchemy database sessions

**Commented Endpoints** (currently disabled):
- `/google/login` - Initiates Google OAuth authorization flow
- `/google/callback` - Handles OAuth callback with:
  - Token validation and user info extraction
  - Database lookup/creation of `ExternalUser` records
  - JWT token generation using user_id and email claims
  - Returns access token to frontend

## Important Logic
1. **User Persistence**: Checks if Google user exists; creates new record if not
2. **JWT Generation**: Creates signed JWT tokens with user identity for session management
3. **Error Handling**: Validates Google login response, raises 400 on failure

**Note**: Core OAuth endpoints are commented out—implementation is incomplete or being refactored.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary: Gifts API Router

## Purpose
FastAPI router for managing gifts with CRUD operations, authentication, and database integration.

## Key Logic
- **Authentication**: Validates JWT tokens from Authorization headers
- **Database Operations**: Uses SQLAlchemy ORM to query/manipulate gifts in database
- **Dynamic Filtering**: Supports searching gifts by any column (id, name, brand, size, color, user_id) with case-insensitive matching

## Important Functions/Endpoints

1. **`get_db()`** - Dependency injection function that manages database session lifecycle

2. **`GET /gifts/fetch/{user_id}`** - Retrieves all gifts for a user
   - Requires valid JWT token
   - Returns 404 if user/gifts not found, 401 if auth missing/invalid

3. **`GET /gifts/searchby/{column}/{value}`** - Searches gifts by column
   - Validates column against whitelist (prevents SQL injection)
   - Uses dynamic attribute lookup via `getattr()`
   - Case-insensitive, whitespace-trimmed search

4. **`POST /gifts/add/{user_id}`** - Creates new gift (partially shown)
   - Requires authorization header
   - Uses `GiftTemplate` schema for validation

## Key Components
- **Pydantic Models**: `GiftCreate`, `GiftPatch`, `GiftResponse` for request/response validation
- **SQLAlchemy Models**: `Gifts`, `User` for database entities
- **Auth Utils**: JWT token verification via `verify_token()`](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Summary

**Purpose:** FastAPI router for managing sharable gift list links. Allows users to create shareable URLs for their gift lists and retrieve gifts via share tokens.

**Key Logic:**
- Creates unique sharable links tied to gift lists with auto-generated share tokens
- Retrieves gift lists and associated gifts using a share token for public access

**Main Functions:**

1. **`create_sharable_links(user_id)`** - POST endpoint
   - Creates a new `GiftsList` record for a user
   - Generates and returns a shareable URL with the auto-generated `share_token`
   - Includes SQLAlchemy error handling with rollback

2. **`get_gifts(token)`** - GET endpoint
   - Queries gift list by `share_token`
   - Returns 401 error if token invalid
   - Fetches all gifts belonging to the list owner
   - Returns owner ID and associated gifts

**Dependencies:** SQLAlchemy ORM, FastAPI dependency injection for database sessions](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# User Management API Router

## Purpose
FastAPI router for user authentication and management, including registration, login, token verification, and user search functionality.

## Key Logic

**Authentication Flow:**
- Uses OAuth2 with JWT tokens for securing endpoints
- `get_current_user()` dependency validates JWT tokens and retrieves authenticated user from database
- Password hashing via `hash_password()` utility for secure storage

**Main Endpoints:**

1. **`/search/{id}`** - Retrieves user by ID from database
2. **`/post`** - Creates new user (basic creation without password hashing)
3. **`/register`** - User registration with:
   - Duplicate email validation
   - Password hashing before storage
   - Returns newly created user
4. **`/login/basic`** - Incomplete endpoint (truncated code)

## Important Components

- **Router**: `APIRouter` with `/users` prefix
- **Dependencies**: Database session (`get_db`), OAuth2 token scheme
- **Models**: `User`, `RefreshTokens`
- **Utilities**: JWT handling (`create_acces_token`, `verify_token`), password hashing
- **Schemas**: `UserCreate`, `UserResponse`, `UserLogin`, `UserGuest`

## Notes
- Code appears incomplete (login endpoint truncated)
- Some commented-out code for alternative token verification
- Mixes direct database queries with list-based search (line with `users_list`)](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Security/Authentication Module Summary

**Purpose:** Handles password hashing and JWT token-based authentication for a FastAPI application.

**Key Logic:**
- Uses bcrypt algorithm via Passlib for secure password hashing
- Implements OAuth2 Bearer token authentication scheme
- Decodes and validates JWT tokens to extract user identity
- Queries database to verify user exists

**Important Functions:**

1. **`hash_password(password)`** - Hashes plain text passwords using bcrypt
2. **`verify_password(plain_password, hashed_password)`** - Compares plain text against stored hash
3. **`get_user(token, db)`** - FastAPI dependency that:
   - Extracts JWT token from request header
   - Decodes token using HS256 algorithm and SECRET_KEY
   - Retrieves email from token payload
   - Queries database for matching user
   - Raises 401 error if token invalid or user not found

**Configuration:**
- `pwd_context` - Passlib context configured for bcrypt with automatic scheme deprecation
- `oauth2_scheme` - OAuth2 Bearer token extractor pointing to "auth/login" endpoint
- `SECRET_KEY = "protected"` ⚠️ (hardcoded - security risk)
- `ALGORITHM = "HS256"` - JWT signing algorithm

**Note:** This is a dependency function meant to be injected into FastAPI route handlers to protect endpoints.](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Authentication Module

**Purpose:** Handles JWT token creation and verification for API authentication.

**Key Logic:**
- Uses HS256 algorithm with a secret key for token signing
- Tokens expire after 30 minutes by default
- Supports custom expiration times via `expires_delta` parameter

**Important Functions:**

1. **`create_acces_token(data, expires_delta)`** - Generates a signed JWT token
   - Copies input data and adds expiration claim (`exp`)
   - Returns encoded token string

2. **`verify_token(token)`** - Validates and decodes a JWT token
   - Returns payload dictionary if valid
   - Returns `None` on decoding errors (invalid/expired tokens)

**Note:** The function name has a typo (`create_acces_token` should be `create_access_token`). Also, using a hardcoded secret key in production code is a security risk—should use environment variables.](#\utils\jwthandlerspy)

---


---

