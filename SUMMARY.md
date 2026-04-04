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

**Purpose:** Sets up SQLAlchemy database connection and session management for a PostgreSQL database (AWS RDS).

**Key Components:**

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance using credentials and `create_engine()`
   - Engine serves as the core interface to the database

2. **Session Factory**
   - `SessionLocal = sessionmaker()` creates a factory for database sessions
   - Sessions handle ORM operations and queries
   - Global `db` instance created (though typically should be lazily generated per request)

3. **ORM Base**
   - `Base = declarative_base()` creates the base class all models inherit from
   - Enables SQLAlchemy to map Python classes to database tables

4. **Key Functions:**
   - `init_db()`: Creates all database tables defined in models
   - `get_db()`: Generator function for dependency injection; yields session and ensures cleanup via finally block

**Security Note:** Database credentials are hardcoded (should use environment variables instead).](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary: FastAPI Application Entry Point

## Purpose
This is the main application file for "Gifters" — a gift management backend API built with FastAPI.

## Key Setup
- **CORS Configuration**: Allows cross-origin requests from `localhost:3000` (frontend), with credentials and all HTTP methods/headers enabled
- **Database Initialization**: Calls `init_db()` to set up the database on startup
- **Router Registration**: Includes four route modules for handling different features:
  - `gifts` — gift management endpoints
  - `users` — user management endpoints
  - `share` — sharing functionality
  - `auths` — authentication (currently disabled)

## Important Components
- **Root Endpoint** (`GET /`): Health check that confirms the backend is running
- **Middleware**: CORS layer that injects necessary headers for browser-based cross-origin requests

The app is configured as a standard FastAPI service ready to handle requests from a frontend running on port 3000.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary

## Purpose
A FastAPI REST API server for a "Gifters" application that provides endpoints for greeting users, searching/listing gifts, and retrieving user information.

## Key Components

**Framework Setup:**
- FastAPI app with title "Gifters API" and version 0.1
- Uses Pydantic's `BaseModel` for request body validation (similar to TypeScript types)

**Endpoints:**

1. **Basic Routes:**
   - `GET /` - Returns greeting message
   - `GET /ping` - Health check

2. **Path Parameters:**
   - `GET /greet/{name}` - Simple greeting
   - `GET /greet-adv/{name}` - Advanced greeting with optional query params (`excited`, `times`)

3. **Request Body:**
   - `POST /echo` - Echoes text repeated N times using `EchoPayload` schema validation

4. **Search/Filter:**
   - `GET /gifts/search` - Filters mock gift data by optional `brand` and `max_price` query params
   - `GET /gifts` - Returns all mock gifts

5. **User Data:**
   - `GET /user/{user_id}` - Returns mock user by ID
   - `GET /users/db/{user_id}` - Returns user from mock database list (code appears truncated)

## Key Logic
- Query parameter validation using `Optional[Type]` for optional filters
- List comprehension for filtering gifts based on brand and price
- Automatic JSON serialization of returned dictionaries
- Mock data storage (not connected to a real database)](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

**Purpose:** SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models:

1. **User** - Core user entity
   - Supports multiple auth providers (local, Google, guest)
   - Stores email, name, hashed password, auth metadata
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Individual gift items
   - Contains gift details (name, brand, size, color, price, link, notes)
   - `claimed` flag tracks if gift is reserved
   - Foreign key to User (owner)
   - Tracks both owner and claimer relationships

3. **GiftsList** - Shareable gift collections
   - Groups gifts per user
   - Auto-generates unique `share_token` (UUID) for sharing lists
   - Links back to User

4. **RefreshTokens** - JWT token storage
   - Stores refresh tokens for session management
   - References User via foreign key

5. **ExternalUser** - OAuth user cache
   - Stores Google OAuth user data (google_id, name, email)
   - Tracks creation timestamp

**Key Features:**
- Multi-provider authentication (local credentials, Google OAuth, guest mode)
- Bidirectional relationships using `back_populates` for convenient data access
- Automatic timestamps using UTC timezone
- UUID-based shareable gift list tokens](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Summary: Gifters Backend Deployment Guide

## Purpose
Documentation and instructions for deploying a FastAPI backend application to AWS infrastructure with database management.

## Key Sections

### 1. **Database Migration (Alembic)**
- Commands to generate and apply schema migrations
- Adds new columns to existing tables (e.g., hashed password to users)
- `alembic upgrade head` applies pending migrations

### 2. **AWS RDS Setup**
- Host PostgreSQL/database on AWS RDS
- Extract connection credentials (host, port, etc.) to configure backend

### 3. **AWS EC2 Deployment**
- Launch Ubuntu instance on EC2
- Configure **Key Pair**: SSH authentication for remote access
- Configure **Security Groups**: Firewall rules for inbound/outbound traffic

### 4. **EC2 Instance Setup**
- Install dependencies: Python, pip, venv, git, nginx
- Clone repository
- Create isolated virtual environment
- Install requirements and run Uvicorn on port 8000

### 5. **24/7 Service Management (Systemd)**
- Create `/etc/systemd/system/fastapi.service` file
- Configures FastAPI to run as background service with auto-restart
- Key settings:
  - Runs as `ubuntu` user
  - Points to venv Python interpreter
  - Auto-restarts on failure
  - Starts on system boot

### **Important Commands**
```bash
systemctl daemon-reload  # Reload service configs
systemctl start/stop/restart/status fastapi  # Service control
```

**Result**: Backend accessible 24/7 at EC2 public IP on port 8000](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Code Summary: Pydantic Schemas

**Purpose:** Defines request/response validation schemas for a gift registry API using Pydantic models.

**Key Components:**

1. **User Schemas:**
   - `UserCreate` - Registration payload (name, email, password)
   - `UserLogin` - Login payload (email, password)
   - `UserGuest` - Social login payload (email, name, provider_id)
   - `UserResponse` - User data response (id, name, email with ORM mode enabled)

2. **Authentication Response:**
   - `GuestResponse` - Returns authenticated user + JWT access token

3. **Gift Schemas:**
   - `GiftTemplate` - Gift creation input (name, optional brand/size/color/link/note, price)
   - `GiftResponse` - Full gift object response (inherits from GiftTemplate, adds id, user_id, claimed status with ORM mode)
   - `GiftOut` - Minimal gift view (id, claimed status, claimed_by username for public sharing)

**Important Details:**
- All schemas use `orm_mode = True` to automatically convert SQLAlchemy ORM objects to Pydantic models
- Gift price is stored as `int` (likely cents to avoid floating-point issues)
- Optional fields allow flexible gift creation and updates](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Marks the containing directory as a Python package, allowing it to be imported as a module
- Currently empty (no code executed or symbols exported)
- This is a standard Python convention required for package recognition in Python versions < 3.3 (technically optional in 3.3+ with namespace packages, but still widely used)

**No functions or components** - this is just a marker file.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

## Purpose
This file sets up a FastAPI web application server for a "Gifters" application.

## Key Components
- **FastAPI app initialization**: Creates the main FastAPI application with the title "Gifters"
- **Router inclusion**: Imports and registers the `gifts` router from the `routes` module to handle gift-related endpoints

## Important Logic
The file serves as the application's entry point, establishing the foundational server setup and routing infrastructure. The actual endpoint logic is delegated to the `gifts` router module.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary

**Purpose:** FastAPI authentication router that handles Google OAuth2 integration with JWT token generation.

**Key Logic:**
- Sets up OAuth2 configuration for Google login using credentials from environment variables
- Provides database session dependency injection via `get_db()`
- Includes database models for storing external users (ExternalUser)

**Important Components:**
- `oauth.register()` - Configures Google OAuth2 client with required endpoints and scopes (openid, email, profile)
- `get_db()` - Dependency function that yields database sessions and ensures cleanup
- **Commented endpoints:**
  - `/google/login` - Would initiate Google OAuth flow
  - `/google/callback` - Would handle OAuth callback, storing user in DB and generating JWT token

**Current State:** The Google login/callback endpoints are commented out, so the router is essentially inactive. When enabled, it would create/retrieve users from the database and issue JWT tokens for authenticated users.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Code Summary: FastAPI Gifts Management Router

## Purpose
This file defines REST API endpoints for managing gifts in a FastAPI application. It handles fetching, searching, and adding gifts with authentication and database integration.

## Key Components

**Pydantic Models** (Data Validation):
- `GiftCreate`: Input schema for creating gifts (name, brand, size, color)
- `GiftPatch`: Partial update schema with optional fields
- `Gift`: Full gift object including ID
- `GiftDataBase`: Wrapper for list of gifts

**Database Helper**:
- `get_db()`: Dependency that manages SQLAlchemy session lifecycle (yields connection, closes on completion)

## Important Endpoints

1. **`GET /gifts/fetch/{user_id}`** - Fetch all gifts for a user
   - Requires JWT token in Authorization header
   - Validates token before returning gifts filtered by user_id
   - Returns 404 if user not found, 401 if token invalid

2. **`GET /gifts/searchby/{column}/{value}`** - Search gifts by any field
   - Validates column against whitelist (id, name, brand, size, color, user_id)
   - Case-insensitive search with whitespace trimming
   - Uses dynamic attribute lookup via `getattr()`
   - Returns 404 if no matches found

3. **`POST /gifts/add/{user_id}`** - Add gift for a user (incomplete)
   - Requires Authorization header
   - Accepts `GiftTemplate` request body

## Key Logic
- **Authentication**: Token extraction and validation from Bearer token format
- **Security**: Whitelist validation for search columns to prevent SQL injection
- **Case-insensitive search**: Uses `func](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Code Summary

## Purpose
FastAPI router for creating and accessing sharable gift list links. Allows users to generate unique share tokens for their gift lists and retrieve gifts via those tokens.

## Key Logic

**Create Sharable Link** (`POST /{user_id}`):
- Creates a new `GiftsList` record with the given user_id
- Auto-generates a `share_token` (via model)
- Returns a sharable URL with the token
- Includes error handling with SQLAlchemy exception rollback

**Get Gifts by Token** (`GET /token/{token}`):
- Looks up a `GiftsList` by `share_token`
- Returns 401 if token doesn't exist
- Fetches all gifts for that list's owner
- Returns owner user_id and associated gifts

## Important Functions/Components

| Component | Purpose |
|-----------|---------|
| `create_sharable_links()` | POST endpoint to generate new gift list share tokens |
| `get_gifts()` | GET endpoint to retrieve gifts via share token |
| `router` | APIRouter with `/share` prefix for route organization |
| `Depends(get_db)` | Dependency injection for database session |

**Note:** The UUID import is unused; likely intended for token generation (which appears handled by the model instead).](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# Summary: User Authentication & Management API Router

## Purpose
FastAPI router handling user registration, login, and authentication with JWT tokens and password hashing.

## Key Logic

**Authentication Flow:**
- `get_current_user()` - Dependency that validates JWT tokens from request headers, decodes them, and retrieves the authenticated user from the database
- Uses OAuth2 Bearer token scheme for API security

**Core Endpoints:**

1. **`/search/{id}`** (GET) - Fetches a specific user by ID
2. **`/post`** (POST) - Creates a new user (stores raw password - security issue)
3. **`/register`** (POST) - Registers new user with:
   - Email uniqueness validation
   - Password hashing via `hash_password()`
   - Stores both plain and hashed password (unnecessary redundancy)
4. **`/login/basic`** (POST) - *Incomplete in provided code*

## Important Components

- **Dependencies**: `get_db` (database session), `oauth2_scheme` (OAuth2 token extraction)
- **JWT Handling**: Token decode/verify using `jose` library with SECRET_KEY and ALGORITHM
- **Database Models**: `User`, `RefreshTokens` 
- **Schemas**: `UserCreate`, `UserResponse`, `UserLogin`, `UserGuest`
- **Utils**: Password hashing/verification, JWT token creation

## Security Notes
⚠️ Storing plain passwords alongside hashed passwords is a vulnerability—should only store hashed versions.](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Code Summary: Authentication & Security Module

## Purpose
Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Securely hashes passwords using bcrypt_sha256
- `verify_password()` - Validates plain text passwords against hashed versions
- Uses Passlib's `CryptContext` with automatic deprecation handling for algorithm upgrades

**JWT Authentication:**
- `oauth2_scheme` - OAuth2 password bearer token scheme for FastAPI
- `SECRET_KEY` & `ALGORITHM` - Configuration for JWT token encoding/decoding (HS256)

**User Validation:**
- `get_user()` - FastAPI dependency that:
  - Extracts JWT token from request headers
  - Decodes and validates token using SECRET_KEY
  - Queries database for user by email (from token "sub" claim)
  - Raises HTTP 401 exception if token invalid or user not found
  - Returns authenticated User object

## Important Logic
- Uses dependency injection (`Depends()`) to automatically validate tokens on protected endpoints
- Handles JWT decode errors gracefully with standard HTTP 401 response
- Integrates with SQLAlchemy ORM for database queries

⚠️ **Security Note:** `SECRET_KEY = "protected"` is hardcoded and should use environment variables in production.](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles JWT (JSON Web Token) creation and verification for authentication.

**Key Components:**

1. **Configuration Constants:**
   - `SECRET_KEY`: Signing key for JWT encoding/decoding
   - `ALGORITHM`: HS256 (HMAC SHA-256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30-minute token lifespan

2. **`create_acces_token(data, expires_delta)`** - Creates JWT token
   - Copies input data, adds expiration timestamp
   - Encodes using SECRET_KEY and HS256
   - Allows custom expiration or defaults to 30 minutes

3. **`verify_token(token)`** - Validates JWT token
   - Decodes token using SECRET_KEY
   - Returns payload if valid, `None` if JWTError occurs (expired/tampered token)

**Note:** Code has a typo in function name (`create_acces_token` → should be `create_access_token`). Also, hardcoded SECRET_KEY should be moved to environment variables for security.](#\utils\jwthandlerspy)

---


---

