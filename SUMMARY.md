# gifters-backend Code Summary

**Repository name: gifters-backend

**Total files analyzed: 15 

------------

# Table of contents 

- [\database.py](#\databasepy)
- [\main.py](#\mainpy)
- [\mainlearn.py](#\mainlearnpy)
- [\models.py](#\modelspy)
- [\README.md](#\readmemd)
- [\schemas.py](#\schemaspy)
- [\SUMMARY.md](#\summarymd)
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
Database configuration and initialization module for a gift-tracking application using SQLAlchemy ORM with PostgreSQL.

## Key Components

1. **Database Connection**
   - Configures PostgreSQL connection to AWS RDS instance
   - Creates engine and sessionmaker for database operations

2. **Core Objects**
   - `engine`: Database connection pool
   - `SessionLocal`: Factory for creating DB sessions
   - `Base`: Declarative base class for all ORM models to inherit from

3. **Key Functions**
   - `init_db()`: Creates all database tables based on defined models
   - `get_db()`: Generator that provides DB sessions with automatic cleanup (for dependency injection in FastAPI)

4. **Mock Data** (for testing)
   - `gifts_mock`: Sample gift items with id, name, brand, price
   - `users_list`: Sample users with id, name, email

## Important Notes
⚠️ **Security Issue**: Database credentials (password, host) are hardcoded in source code—should use environment variables instead.](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI-based "Gifters" backend application - a gift management system with user and sharing features.

**Key Components:**

1. **CORS Configuration** - Enables cross-origin requests from `localhost:3000` (frontend), allowing credentials and all HTTP methods/headers
2. **Database Initialization** - Calls `init_db()` to set up database on startup
3. **Route Registration** - Includes routers for:
   - `gifts` - Gift management endpoints
   - `users` - User management endpoints
   - `share` - Sharing functionality
   - `auths` - Authentication (currently disabled)

4. **Root Endpoint** - Simple GET `/` health check returning a success message

**Architecture:** Standard FastAPI app setup with middleware, database initialization, and modular route organization.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
FastAPI-based REST API for a gift management system with search, listing, and user endpoints.

## Key Components

**Framework & Setup:**
- FastAPI application with Pydantic models for request validation
- `EchoPayload` model defines schema for echo endpoint (text + repeat count)

**Endpoints:**

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Root health check |
| GET | `/ping` | Ping/status endpoint |
| GET | `/greet/{name}` | Simple greeting with path parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with query params (excited, times) |
| POST | `/echo` | Echoes text N times (validates body with EchoPayload) |
| GET | `/gifts` | List all gifts (mock data) |
| GET | `/gifts/search` | Filter gifts by brand & max_price (optional query params) |
| GET | `/user/{user_id}` | Get single user by ID |
| GET | `/users/db/{user_id}` | Get user from mock DB |

## Important Logic
- **Query filtering** (`/gifts/search`): Filters mock gift list using Python list comprehension with optional parameters
- **Path/query parameters**: Demonstrates FastAPI's automatic type validation and parameter extraction
- **Request body validation**: `EchoPayload` enforces required fields and defaults
- **Mock data**: All endpoints return hardcoded sample data (no real database)

## Status
Work-in-progress (v0.1) — endpoints are partially implemented with mock data only.](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary: SQLAlchemy Database Models

## Purpose
Defines the database schema for a gift-sharing application using SQLAlchemy ORM, including user authentication, gift management, and sharing functionality.

## Key Models

**User**
- Core user entity with email, hashed password, and name
- Supports multiple auth providers (local, Google, guest)
- One-to-many relationship with Gifts and GiftsList

**Gifts**
- Represents individual gift items with details (name, brand, size, color, price, link)
- Tracks claim status via `claimed` boolean flag
- Foreign key to User (owner) and relationship to claimer
- Price stored as integer (likely cents)

**GiftsList**
- Creates shareable gift lists per user
- Uses UUID for unique `share_token` enabling public list sharing
- One-to-many with User

**RefreshTokens**
- Stores JWT refresh tokens for session management
- Links tokens to users via foreign key

**ExternalUser**
- Tracks OAuth users (Google authentication)
- Stores Google ID and basic user info

**AuthProvider Enum**
- Defines authentication types: local, Google, guest, user

## Key Logic
- Relationships use `back_populates` for bidirectional navigation (e.g., User ↔ Gifts)
- Timestamps default to UTC
- Share tokens auto-generate as UUIDs for gift list sharing](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Summary: Gifters Backend Deployment Guide

## Purpose
Documentation for deploying a FastAPI backend application to AWS, including database setup, EC2 hosting, and production service configuration.

## Key Sections

### 1. **Database Management (Alembic)**
- Commands to generate and apply database migrations
- Adds/modifies columns in existing tables
- Example: Adding hashed password column to users table

### 2. **AWS RDS Setup**
- Host PostgreSQL/MySQL database on AWS RDS
- Configure connection credentials (host, port, etc.)
- Connect backend to remote database

### 3. **AWS EC2 Instance Setup**
- Launch EC2 instance for backend hosting
- Configure **Key Pair**: SSH authentication for instance access
- Configure **Security Groups**: 
  - Inbound rules: control incoming traffic
  - Outbound rules: control outgoing connections

### 4. **EC2 Environment Setup**
Install dependencies:
- **python3-pip**: Package manager
- **python3-venv**: Isolated Python environments
- **git**: Clone repositories
- **nginx**: Production web server (reverse proxy)

### 5. **Application Deployment**
- Clone repository
- Create virtual environment
- Install dependencies via `requirements.txt`
- Run Uvicorn: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 6. **Production Service (Systemd)**
- Create systemd service file to run FastAPI 24/7
- Auto-restart on failure
- Manage via: `systemctl start/stop/restart/enable/status fastapi`

## Result
FastAPI backend accessible at `http://<EC2-Public-IP>:8000` with](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Code Summary: Pydantic Schemas

**Purpose:** Defines request/response validation schemas for a gift-sharing application with user authentication and guest access.

**Key Components:**

1. **User Schemas:**
   - `UserCreate`: Registration input (name, email, password)
   - `UserLogin`: Login credentials (email, password)
   - `UserGuest`: OAuth/social login (email, name, provider_id)
   - `UserResponse`: API response with user details (excludes password)

2. **Authentication:**
   - `GuestResponse`: Returns user data + access token for authenticated sessions

3. **Gift Schemas:**
   - `GiftTemplate`: Base gift creation model with optional fields (brand, size, color, link, note, price)
   - `GiftResponse`: Full gift object with ID, user ownership, and claimed status
   - `GiftOut`: Minimal gift view showing claim status and claimer name

**Important Features:**
- All schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to responses
- Optional fields use `Optional[type] = None` for flexible input
- Price stored as `int` (likely cents to avoid float precision issues)
- Separates internal models (full details) from public responses (sensitive data excluded)](#\schemaspy)

---

- [\SUMMARY.md](#\summarymd)
- [# Gifters-Backend - High-Level Summary

## **Purpose**
Gifters is a FastAPI-based backend REST API for a gift-sharing/recommendation platform. It manages users, gifts, sharing functionality, and authentication.

---

## **Architecture Overview**

| Layer | Files | Purpose |
|-------|-------|---------|
| **Core App** | `main.py`, `app/main.py` | FastAPI initialization, CORS setup, route registration |
| **Database** | `database.py` | PostgreSQL (AWS RDS) connection, SQLAlchemy ORM session management |
| **Models** | `models.py` | ORM entity definitions (Users, Gifts, etc.) |
| **Schemas** | `schemas.py` | Pydantic request/response validation models |
| **Routes** | `routes/` | API endpoints (gifts, users, sharing, auth) |
| **Utils** | `utils/` | JWT authentication, token handling |

---

## **Key Features**

✅ **Authentication** - JWT-based token handling (`jwt_handlers.py`)  
✅ **Gift Management** - CRUD operations on gifts (`routes/gifts.py`)  
✅ **User Management** - User profiles and data (`routes/users.py`)  
✅ **Sharing System** - Gift sharing functionality (`routes/share.py`)  
✅ **Security** - CORS enabled, auth utilities available  

---

## **Critical Issues**
⚠️ **Hardcoded DB credentials** in `database.py` - should use environment variables  
⚠️ **Auth routes currently disabled** in main.py

---

## **Frontend Integration**
CORS configured to accept requests from `localhost](#\summarymd)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Marks the containing directory as a Python package, allowing it to be imported as a module
- Currently empty - no code is executed or exported
- Enables the use of `from package import module` syntax

**Use Case:** Standard Python convention for package structure. When present, Python treats the directory as a namespace package rather than a regular folder.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Entry point for a FastAPI web application called "Gifters"

**Key Logic:**
- Creates a FastAPI application instance with the title "Gifters"
- Registers a router from the `routes.gifts` module to handle gift-related endpoints

**Components:**
- `app`: FastAPI application instance that serves as the main application object
- `gifts.router`: Router imported from a separate module that contains gift-related API routes

This is a minimal main application file that delegates route handling to a modular router structure.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary

**Purpose:** FastAPI authentication module for Google OAuth2 integration with JWT token generation.

**Key Logic:**
- Configures Google OAuth2 client using environment variables (client ID, secret, redirect URI)
- Implements database session dependency injection via `get_db()`
- Contains commented-out OAuth flow endpoints that would:
  1. Redirect users to Google login
  2. Handle Google callback with token exchange
  3. Store/retrieve user in `ExternalUser` database table
  4. Generate JWT token for authenticated sessions

**Important Components:**
- `OAuth` client configured for Google with email/profile scopes
- `get_db()`: Dependency for database session management
- Commented endpoints: `google_login()` and `google_callback()` (currently disabled)
- JWT generation using HS256 algorithm with user_id, email, and role claims

**Status:** Incomplete implementation - OAuth endpoints are commented out, suggesting this is work-in-progress or temporarily disabled code.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary

## Purpose
FastAPI router for managing gifts with CRUD operations. Handles fetching, searching, and adding gifts with JWT authentication and database persistence.

## Key Logic

**Authentication**: Validates JWT tokens from Authorization headers on protected endpoints.

**Database Operations**:
- `fetch_gifts()`: Retrieves all gifts for a user (requires valid JWT token)
- `gifts_search()`: Searches gifts by column (name, brand, size, color, id, user_id) with case-insensitive matching
- `add_gift()`: Creates new gift entries (incomplete in snippet)

**Security**: 
- Token verification via `verify_token()`
- SQL injection prevention using SQLAlchemy ORM and `getattr()` with allowed columns whitelist
- Authorization header validation

## Important Components

- **Pydantic Models**: `GiftCreate`, `Gift`, `GiftPatch` for request/response validation
- **Database Helper**: `get_db()` dependency for session management
- **Router**: `/gifts` prefix with endpoints for fetch, search, add operations
- **Error Handling**: HTTPException for missing auth (401), invalid tokens, not found (404)

**Note**: The `add_gift()` endpoint definition is incomplete in the provided code.](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Code Summary

## Purpose
FastAPI router that handles shareable gift list links, allowing users to create unique share tokens and retrieve gift lists via those tokens.

## Key Logic

**POST endpoint** (`/{user_id}`):
- Creates a new `GiftsList` record with a user ID
- Database auto-generates a unique `share_token` for the list
- Returns a shareable URL containing the token
- Includes error handling for database failures

**GET endpoint** (`/token/{token}`):
- Looks up a gift list by its share token
- Retrieves all gifts belonging to that list's owner
- Returns owner ID and associated gifts
- Raises 401 error if token doesn't exist

## Important Components
- **APIRouter**: Mounted at `/share` prefix for sharable link operations
- **Database dependency injection**: Uses `get_db()` for session management
- **Models used**: `GiftsList` (stores user_id + auto-generated share_token) and `Gifts`
- **Error handling**: SQLAlchemy exception catching with rollback on create endpoint](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# Code Summary

**Purpose:** FastAPI user authentication router handling user registration, login, and token-based access control.

**Key Components:**

1. **Authentication Dependency (`get_current_user`):**
   - Validates JWT tokens from request headers
   - Decodes token using SECRET_KEY and extracts user_id
   - Queries database for user and raises 401 error if invalid/expired
   - Used as dependency for protected endpoints

2. **User Endpoints:**
   - **`/search/{id}`** - Retrieves a specific user by ID
   - **`/post`** - Creates a user (basic creation)
   - **`/register`** - User registration with password hashing and duplicate email check
   - **`/login/basic`** - (Incomplete) Login endpoint

3. **Security Features:**
   - OAuth2 password bearer token scheme
   - Password hashing using `hash_password()` utility
   - JWT token validation using jose library
   - Email uniqueness validation during registration

4. **Dependencies:**
   - SQLAlchemy ORM for database operations
   - FastAPI security modules for authentication
   - Custom JWT handlers and password utilities

**Status:** Code appears incomplete (login endpoint cut off) and has some inefficiencies (mixed database/list queries, storing both plain and hashed passwords).](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Summary: Authentication & Security Module

## Purpose
Handles user authentication, password hashing, and JWT token validation for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256
- `verify_password()` - Validates plain text password against stored hash

**JWT Token Security:**
- `oauth2_scheme` - OAuth2 bearer token extraction from request headers
- `SECRET_KEY` & `ALGORITHM` - JWT signing credentials (HS256)

**Main Logic:**
- `get_user()` - FastAPI dependency that:
  1. Extracts JWT token from request header (via `oauth2_scheme`)
  2. Decodes token using SECRET_KEY
  3. Retrieves email from token payload
  4. Queries database for matching user
  5. Returns user or raises 401 HTTPException if invalid

## Security Notes
- Uses bcrypt for password hashing with auto-deprecation support
- JWT validation guards endpoints requiring authentication
- Returns 401 "Could not validate credentials" for invalid/missing tokens](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Authentication Module

**Purpose:** Handles JWT token creation and verification for API authentication.

**Key Components:**

1. **Configuration Constants:**
   - `SECRET_KEY`: Signing key for JWT tokens
   - `ALGORITHM`: HS256 hash algorithm
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Default token validity (30 min)

2. **`create_acces_token(data, expires_delta)`** (note: typo in function name)
   - Creates JWT tokens with custom or default expiration
   - Adds expiration claim ('exp') to payload
   - Returns encoded token string

3. **`verify_token(token)`**
   - Decodes and validates JWT tokens
   - Returns payload dict if valid, `None` if JWTError occurs
   - Silent failure on invalid tokens

**⚠️ Security Issues:**
- Hardcoded secret key should use environment variables
- No exception handling details (logging)
- Token errors silently fail instead of raising exceptions](#\utils\jwthandlerspy)

---


---

