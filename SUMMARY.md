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
- [# Summary

**Purpose:** Database configuration and initialization file for a gift management application using PostgreSQL.

**Key Logic:**
- Establishes PostgreSQL connection to AWS RDS using SQLAlchemy ORM
- Sets up session factory for database interactions
- Provides database initialization and session management utilities

**Important Components:**

1. **Database Connection**
   - `DATABASE_URL`: PostgreSQL connection string to AWS RDS instance
   - `engine`: Core database connection interface

2. **Session Management**
   - `SessionLocal`: Factory for creating new ORM sessions
   - `get_db()`: Generator function providing session dependency injection with automatic cleanup

3. **ORM Setup**
   - `Base`: Declarative base class inherited by all ORM models
   - `init_db()`: Creates all tables defined in models

4. **Mock Data**
   - `gifts_mock`: Sample gift catalog (3 items with id, name, brand, price)
   - `users_list`: Sample user data (3 users with id, name, email)

**Note:** Credentials are hardcoded (security risk - should use environment variables).](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI backend application called "Gifters" - likely a gift management/sharing system.

**Key Components:**

1. **CORS Middleware Configuration**
   - Allows cross-origin requests from `http://localhost:3000` (frontend dev server)
   - Enables credentials and permits all HTTP methods/headers

2. **Database Initialization**
   - Calls `init_db()` to set up the database on startup

3. **Route Registration**
   - Includes routers for: gifts, users, share functionality
   - Auths router commented out (possibly under development)

4. **Root Endpoint**
   - Simple health check GET `/` that returns a success message

**Key Logic:** Minimal business logic here—this is purely API setup and configuration. The actual functionality is delegated to imported routers (gifts, users, share, auths).](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
A FastAPI-based REST API for a gift management system. Provides endpoints for greeting users, searching/listing gifts, echoing text, and retrieving user information.

## Key Components

**Data Models:**
- `EchoPayload`: Pydantic schema validating POST request body with `text` (required) and `repeat` (optional, default=1)

**Core Endpoints:**

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Root health check |
| GET | `/ping` | Status check |
| GET | `/greet/{name}` | Basic greeting with path parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with optional query params (`excited`, `times`) |
| POST | `/echo` | Repeats text based on payload |
| GET | `/gifts` | Returns hardcoded gift list |
| GET | `/gifts/search` | Filters gifts by optional `brand` and `max_price` query params |
| GET | `/user/{user_id}` | Mock user lookup by ID |
| GET | `/users/db/{user_id}` | Fetch user from mock database (incomplete) |

## Important Logic
- **Query filtering**: `/gifts/search`](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
Defines SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models

**User**
- Core user entity with email, password, name
- Supports multiple auth providers (local, Google, guest)
- One-to-many relationship with Gifts and GiftsList

**Gifts**
- Gift items with properties: name, brand, size, color, price, link, note
- Includes `claimed` boolean flag to track if gift is reserved
- Foreign key to User (owner)
- One gift belongs to one user

**RefreshTokens**
- Stores JWT refresh tokens for user sessions
- Links tokens to users for authentication validation

**GiftsList**
- Represents shareable gift lists per user
- Auto-generates unique `share_token` (UUID) for sharing
- One user can have multiple gift lists

**ExternalUser**
- Stores Google OAuth user data
- Separate from main User table for external auth tracking

## Important Logic
- **Enum constraints**: `AuthProvider` enum restricts auth types to local/Google/guest/user
- **Relationships**: Back_populates creates bidirectional references without extra DB columns
- **Timestamps**: Auto-populated `created_at` using UTC timezone
- **Unique constraints**: Email](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Gifters-Backend: Deployment & Setup Guide

## **Purpose**
This document outlines the complete setup and deployment pipeline for a FastAPI backend application, covering database migrations, AWS infrastructure setup, and production deployment.

## **Key Sections**

### 1. **Database Migrations (Alembic)**
- Auto-generate schema changes and version control database migrations
- Commands: `alembic revision --autogenerate`, `alembic upgrade head`

### 2. **AWS RDS Database Setup**
- Host PostgreSQL/MySQL in AWS RDS
- Configure connection credentials (host, port, credentials)
- Link database URL to backend environment

### 3. **AWS EC2 Deployment**
- **Key Pair**: SSH authentication for secure instance access
- **Security Groups**: Firewall rules controlling inbound/outbound traffic
- **Instance Setup**: Install Python, pip, venv, git, and nginx dependencies

### 4. **Manual Server Configuration**
- Clone repository, create isolated Python virtual environment
- Install dependencies via `pip install -r requirements.txt`
- Start server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 5. **Production 24/7 Service (Systemd)**
- **Systemd Service File**: Automatically manages](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Summary: schemas.py

**Purpose:** Defines Pydantic validation schemas for request/response data in a gift registry application with user authentication.

**Key Components:**

1. **User Schemas:**
   - `UserCreate`: Registration payload (name, email, password)
   - `UserLogin`: Login credentials (email, password)
   - `UserGuest`: Guest user creation via OAuth (email, name, provider_id)
   - `UserResponse`: User data returned to clients (id, name, email) with ORM mode enabled

2. **Authentication Response:**
   - `GuestResponse`: Returns authenticated user + access token

3. **Gift Schemas:**
   - `GiftTemplate`: Base gift item with optional fields (brand, size, color, link, note, price)
   - `GiftResponse`: Full gift object extending template, includes id, user_id, and claim status
   - `GiftOut`: Minimal gift representation for listing (id, claimed status, claimed_by name)

**Important Details:**
- All response schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to Pydantic models
- Optional fields use `Optional[str] = None` syntax for flexible data
- Inheritance used (`GiftResponse` extends `GiftTemplate`) to reduce duplication](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is an `__init__.py` file, which marks the containing folder as a Python package.

**Key Logic:** None - this is an empty initialization file.

**Important Components:** None - serves only to signal to Python that the directory should be treated as a package, enabling imports from modules within it.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose**: Entry point for a FastAPI application called "Gifters"

**Key Logic**:
- Creates a FastAPI application instance with the title "Gifters"
- Registers a router from the `routes.gifts` module to handle gift-related endpoints

**Components**:
- `app`: FastAPI application instance
- `gifts.router`: Router containing gift-related API routes (imported from `routes/gifts.py`)

This is a minimal main file that sets up the API and mounts gift management routes.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary: Google OAuth Authentication Module

## Purpose
FastAPI authentication router that handles Google OAuth 2.0 login flow for external users, including token generation and user management.

## Key Components

**OAuth Configuration:**
- Registers Google as OAuth provider with client credentials from environment variables
- Configures Google's OAuth endpoints and required scopes (openid, email, profile)

**Database Dependency:**
- `get_db()`: Dependency injection function providing database session management with proper cleanup

**Commented Implementation:**
The actual login flow is currently disabled but includes:
1. **Google Login** (`/google/login`): Initiates OAuth redirect to Google
2. **Google Callback** (`/google/callback`): Handles OAuth response by:
   - Extracting user info from Google's ID token
   - Creating or retrieving `ExternalUser` from database
   - Generating JWT token with user_id, email, and "external" role
   - Returning bearer token to frontend

## Important Logic
- User upsert pattern: Check if Google user exists; create if new, otherwise use existing
- JWT encoding using HS256 algorithm with custom secret
- Token payload structure for role-based access control

**Status:** Code appears to be in development/testing phase with core OAuth endpoints commented out.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Code Summary: FastAPI Gifts Management API

## **Purpose**
REST API router for managing gift records with user authentication and database operations.

## **Key Components**

### **Pydantic Models**
- `GiftCreate`: Input schema (name, brand, size, color)
- `GiftPatch`: Partial update schema (all fields optional)
- `Gift`: Complete gift object with ID

### **Database Functions**
- `get_db()`: Dependency that provides SQLAlchemy session management with cleanup

### **Endpoints**

1. **`GET /gifts/fetch/{user_id}`**
   - Fetches all gifts for a specific user
   - Requires JWT token in Authorization header
   - Validates token before returning data
   - Returns `List[GiftResponse]`

2. **`GET /gifts/searchby/{column}/{value}`**
   - Dynamic search across allowed columns (id, name, brand, size, color, user_id)
   - Case-insensitive filtering with whitespace trimming
   - Uses `getattr()` for dynamic attribute access
   - Returns matching gift records

3. **`POST /gifts/add/{user_id}`** (incomplete)
   - Creates new gift for user
   - Requires Authorization header
   - Input validation via `GiftTemplate`](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Summary

**Purpose:** FastAPI router for managing sharable gift list links, allowing users to create shareable URLs and retrieve gift lists via tokens.

**Key Logic:**
- Creates unique sharable links for gift lists associated with users
- Uses tokens to provide anonymous access to shared gift lists
- Retrieves all gifts belonging to a list owner via a share token

**Important Functions:**

1. **`create_sharable_links(user_id)`** - POST endpoint
   - Creates a new `GiftsList` record for the user
   - Generates a unique `share_token` (auto-created by model)
   - Returns a shareable URL with the token
   - Includes error handling for database failures

2. **`get_gifts(token)`** - GET endpoint
   - Looks up gift list by `share_token`
   - Validates token exists (401 error if not)
   - Retrieves all gifts for the list owner
   - Returns owner ID and associated gifts

**Note:** The code has debug print statements and hardcoded localhost URL suitable for development.](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# User Management API Router

## Purpose
FastAPI router for user authentication and management endpoints, handling registration, login, user search, and token-based authorization.

## Key Components

### Authentication
- **`get_current_user()`** - Dependency that validates JWT tokens from request headers, decodes them, and retrieves the authenticated user from database. Returns 401 error if token is invalid/expired.
- **OAuth2 scheme** - Uses bearer token authentication via `OAuth2PasswordBeaker`

### Endpoints

1. **`GET /search/{id}`** - Retrieves a specific user by ID from database
2. **`POST /post`** - Creates a new user (basic, no validation)
3. **`POST /register`** - User registration with:
   - Email uniqueness validation
   - Password hashing using `hash_password()` utility
   - Stores both plain and hashed password (security issue)
4. **`POST /login/basic`** - Incomplete endpoint (code cuts off)

## Key Logic
- Uses SQLAlchemy ORM for database operations
- JWT token validation via `jose` library
- Password hashing for security
- Email duplicate prevention on registration

## Security Notes
⚠️ **Issues**: 
- Storing plain text password alongside hashed version
- Incomplete login](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Summary

**Purpose:** Authentication and password security utilities for a FastAPI application using JWT tokens and bcrypt hashing.

**Key Components:**

1. **Password Management:**
   - `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm via Passlib
   - `verify_password()` - Validates plaintext password against stored hash

2. **JWT Authentication:**
   - `oauth2_scheme` - OAuth2 password bearer token scheme for extracting tokens from requests
   - `get_user()` - Dependency function that:
     - Extracts JWT token from request header
     - Decodes token using HS256 algorithm and SECRET_KEY
     - Retrieves user email from token payload ("sub" claim)
     - Queries database for matching user
     - Returns authenticated user or raises 401 HTTPException if invalid

3. **Security Config:**
   - Uses bcrypt with automatic deprecation handling for algorithm upgrades
   - HS256 for JWT signing/verification
   - Hardcoded SECRET_KEY (security concern - should use environment variables)

**Main Logic Flow:** Password hashing on registration → JWT token generation on login → Token validation via `get_user()` dependency for protected endpoints.](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles creation and verification of JWT access tokens for authentication.

**Key Components:**

1. **Constants:**
   - `SECRET_KEY`: Signing key for JWT encoding/decoding
   - `ALGORITHM`: HS256 (HMAC-SHA256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Default 30-minute token lifetime

2. **`create_acces_token(data, expires_delta)`** 
   - Creates a signed JWT token from provided data
   - Sets expiration to custom duration or default 30 minutes
   - Returns encoded token string

3. **`verify_token(token)`**
   - Decodes and validates JWT signature
   - Returns token payload (claims) if valid
   - Returns `None` if token is invalid/expired

**Note:** Has a typo in function name (`acces_token` should be `access_token`). The SECRET_KEY should be externalized for security.](#\utils\jwthandlerspy)

---


---

