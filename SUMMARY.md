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

**Purpose:** Database configuration and initialization for a gift-sharing application using PostgreSQL and SQLAlchemy ORM.

**Key Components:**

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance with credentials
   - Creates SQLAlchemy `engine` (core DB interface)

2. **Session Management**
   - `SessionLocal`: Factory for creating DB sessions
   - `get_db()`: Dependency injection function that yields sessions and ensures proper cleanup

3. **ORM Setup**
   - `Base`: Declarative base class for all model definitions
   - `init_db()`: Creates all database tables defined in models

4. **Mock Data**
   - `gifts_mock`: Sample gift items (Shirt, Cap, Shoes)
   - `users_list`: Sample users with contact info

**Key Functions:**
- `init_db()` - Creates database schema
- `get_db()` - Provides clean session handling with try/finally pattern for FastAPI dependency injection

**Note:** Credentials are hardcoded (security risk - should use environment variables).](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary: FastAPI Gifters Backend

**Purpose:** Main entry point for a FastAPI-based backend application called "Gifters" (likely a gift-sharing/management system).

**Key Components:**

1. **CORS Configuration:** Sets up Cross-Origin Resource Sharing to allow requests from `http://localhost:3000` (frontend) with full credentials and method/header flexibility.

2. **Database Initialization:** Calls `init_db()` to set up the database on startup.

3. **Route Registration:** Includes routers from four modules:
   - `gifts` - Gift-related endpoints
   - `users` - User management endpoints
   - `share` - Sharing functionality endpoints
   - `auths` - Authentication (currently disabled/commented out)

4. **Root Endpoint:** Simple health check at `/` returning a success message.

**Important Details:**
- Application title: "Gifters"
- Localhost development setup (port 3000 for frontend)
- Middleware stack includes CORS for browser-based requests
- Clean modular architecture with separated route handlers](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: FastAPI Gifters API

## Purpose
A simple REST API built with FastAPI that provides endpoints for greeting users, echoing text, and searching/retrieving gift products. This is a demonstration API with mock data.

## Key Components

**Framework**: FastAPI with Pydantic validation

**Data Models**:
- `EchoPayload`: Validates POST request body with `text` (required) and `repeat` (optional, default 1)

## Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Root health check |
| GET | `/ping` | Simple status check |
| GET | `/greet/{name}` | Greet user by name |
| GET | `/greet-adv/{name}` | Advanced greeting with `excited` (bool) and `times` (int) query params |
| POST | `/echo` | Echo back text, repeated N times |
| GET | `/gifts/search` | Filter gifts by optional `brand` and `max_price` query params |
| GET | `/gifts` | List all gifts (mock data) |
| GET | `/user/{user_id}` | Get user by ID (mock) |
| GET | `/users/db/{user_id}` | Get user from DB (mock, code incomplete) |

## Key Logic

- **Path parameters**: `{name}`, `{user_id}` extracted from URL
- **Query parameters**: Optional filters with `Optional[T]` type hints
- **Filtering**: List comprehension filters gifts based on brand and max_price conditions
- **String repetition**: `payload.text * repeat` repeats strings

## Notes
- Uses mock data (no real database)
- Automatic](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
SQLAlchemy ORM models for a gift-sharing application database schema. Defines tables for users, gifts, authentication, and gift lists with their relationships.

## Key Models

1. **User** - Core user entity
   - Email-based authentication with hashed passwords
   - Supports multiple auth providers (local, Google, guest)
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Gift items in wishlists
   - Contains product details (name, brand, size, color, price, link)
   - Tracks claimed status
   - Belongs to a User (owner) via foreign key
   - Includes optional notes

3. **GiftsList** - Shareable gift collections
   - Creates curated gift lists per user
   - Generates unique share tokens (UUID) for sharing with others
   - Links back to User

4. **RefreshTokens** - Session management
   - Stores JWT refresh tokens for users
   - Enables persistent authentication

5. **ExternalUser** - OAuth integration
   - Stores Google authentication data (google_id)
   - Separate from main User table for external providers

## Key Features
- **Relationships**: Bidirectional ORM relationships (e.g., user ↔ gifts) for easy data traversal
- **Enums**: `AuthProvider` restricts auth methods to predefined values
- **Defaults**: Timestamps auto-set to UTC, share tokens auto-generated
- **Constraints**: Unique emails/tokens, indexed fields for fast lookups](#\modelspy)

---

- [\README.md](#\readmemd)
- [# gifters-backend Summary

## Purpose
This is a **deployment and setup guide** for a FastAPI backend application, covering database migrations, AWS infrastructure setup, and production deployment.

## Key Sections

### 1. **Database Migrations (Alembic)**
- Commands to generate and apply schema changes
- Example: Adding hashed password column to users table

### 2. **AWS RDS Database Setup**
- Host database in AWS RDS
- Configure connection details (host, port, credentials)

### 3. **AWS EC2 Deployment**
- Launch EC2 instance with proper security configuration
- Install dependencies: Python, pip, venv, git, nginx
- Clone repository and create isolated virtual environment
- Run FastAPI with Uvicorn on port 8000

### 4. **Production Service Management (Systemd)**
- Create systemd service file (`/etc/systemd/system/fastapi.service`)
- Configure Uvicorn to run automatically on system startup
- Enable auto-restart on failures
- Key settings:
  - User: ubuntu
  - Auto-restart with 3-second delay
  - Python unbuffered output for logging

## Important Commands
- `systemctl daemon-reload` - reload service configuration
- `systemctl start/enable/restart/status fastapi` - manage service lifecycle

## Architecture
Local development → Git → EC2 instance → Systemd service → Uvicorn → Port 8000 (accessible via public IP)](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Summary: schemas.py

**Purpose:** Defines Pydantic validation schemas for API request/response serialization across user authentication and gift management endpoints.

**Key Components:**

1. **User Schemas:**
   - `UserCreate`: Registration payload (name, email, password)
   - `UserLogin`: Login credentials (email, password)
   - `UserGuest`: OAuth/social login (email, name, provider_id)
   - `UserResponse`: User data output (id, name, email) with ORM mode enabled for SQLAlchemy compatibility

2. **Authentication:**
   - `GuestResponse`: Combines user data + JWT access token for login responses

3. **Gift Management Schemas:**
   - `GiftTemplate`: Base gift creation schema with optional fields (brand, size, color, link, note, price)
   - `GiftResponse`: Extended template with database fields (id, user_id, claimed status) - inherits from GiftTemplate
   - `GiftOut`: Minimal gift view (id, claimed status, claimed_by user) for public/list endpoints

**Key Feature:** All schemas with `orm_mode = True` allow direct database object serialization, eliminating manual conversion.](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Empty or minimal file that marks its containing directory as a Python package
- Allows the directory to be imported as a module in Python
- No active logic or functions defined

This is a standard convention in Python projects and is typically left empty unless the package needs to expose specific APIs or perform initialization logic at import time.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Entry point for a FastAPI web application called "Gifters"

**Key Components:**
- **FastAPI app instance** - Creates the main application with title "Gifters"
- **Router inclusion** - Registers the `gifts` router from the `routes` module to handle gift-related endpoints

**Functionality:** This is a minimal application setup that delegates all route handling to a separate `gifts` module, following a modular architecture pattern.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# OAuth Authentication Module

**Purpose:** FastAPI authentication router that handles Google OAuth2 login integration.

**Key Components:**

1. **OAuth Registration**
   - Configures Google OAuth2 with credentials from environment variables
   - Sets up authorization and token endpoints
   - Requests scopes: openid, email, profile

2. **Database Helper**
   - `get_db()`: Dependency function that provides SQLAlchemy session management with automatic cleanup

3. **Commented Endpoints** (Currently Disabled)
   - `google_login`: Initiates OAuth redirect to Google
   - `google_callback`: Handles Google's OAuth callback to:
     - Exchange authorization code for access token
     - Extract user info from ID token
     - Create/retrieve user in database (`ExternalUser` model)
     - Generate JWT token for the application
     - Return access token to frontend

**Key Logic Flow:**
Google auth → User lookup/creation in DB → JWT generation → Return token

**Status:** Code is mostly commented out; the OAuth infrastructure is set up but endpoints are not yet active.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary: FastAPI Gifts Management Router

## Purpose
This file defines REST API endpoints for managing gifts in a gift-tracking application. It handles CRUD operations with JWT authentication and database persistence.

## Key Components

### Pydantic Models
- **GiftCreate**: Request schema for creating gifts (name, brand, size, color)
- **GiftPatch**: Optional fields for updating gifts
- **Gift**: Extended GiftCreate with ID
- **GiftResponse**: Database response model

### Database Dependency
- **get_db()**: Dependency injection function that manages SQLAlchemy session lifecycle (creates and closes DB connections)

### Endpoints

1. **GET `/gifts/fetch/{user_id}`**
   - Retrieves all gifts for a specific user
   - Requires JWT token in Authorization header
   - Validates token before returning gifts
   - Returns `List[GiftResponse]`

2. **GET `/gifts/searchby/{column}/{value}`**
   - Searches gifts by dynamic column names
   - Validates column against whitelist (id, name, brand, size, color, user_id)
   - Case-insensitive search with whitespace trimming
   - Returns matching gift records

3. **POST `/gifts/add/{user_id}`** (incomplete)
   - Creates new gift for a user
   - Requires Authorization header (JWT validation)

## Key Logic
- **Dynamic attribute fetching**: Uses `getattr()` for flexible column querying
- **Security**: JWT token verification via Authorization header
- **Input validation**: Whitelist-based column filtering to prevent SQL injection
- **Error handling**: Returns appropriate HTTP status codes (401 for auth, 404 for not found)](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Sharable Links API Summary

**Purpose:** FastAPI router that manages shareable gift list links, allowing users to create unique tokens and retrieve gift lists via those tokens.

## Key Logic

1. **Create Sharable Link** (`POST /{user_id}`)
   - Creates a new `GiftsList` entry with a unique `share_token` for a user
   - Returns a shareable URL containing the token
   - Handles database errors with rollback on failure

2. **Retrieve Gifts by Token** (`GET /token/{token}`)
   - Validates the share token exists
   - Fetches all gifts associated with the gift list owner
   - Returns owner ID and their gift collection

## Important Components

- **Database Session:** Uses dependency injection for SQLAlchemy ORM sessions
- **Error Handling:** Catches `SQLAlchemyError` and returns 500 status; validates tokens with 401 error
- **Models Used:** `GiftsList` (stores user_id + auto-generated share_token) and `Gifts` (user gift items)
- **Token-Based Access:** Share tokens enable anonymous/public access to specific user's gift lists](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# Summary

**Purpose:** FastAPI router for user authentication and management endpoints.

**Key Logic:**
- User registration with password hashing and duplicate email validation
- JWT-based authentication with token verification
- User search by ID and basic user CRUD operations

**Important Functions/Components:**

1. **`get_current_user()`** - Dependency that validates JWT tokens, decodes them, and retrieves the authenticated user from the database. Returns 401 error for invalid/expired tokens.

2. **`search_user(id)`** - GET endpoint to fetch a user by ID from the database.

3. **`register_user()`** - POST endpoint that creates a new user with email uniqueness validation and password hashing via `hash_password()`.

4. **`post_user()`** - POST endpoint to directly create a user from UserCreate schema.

5. **`logi()`** - Incomplete login endpoint (code cuts off).

**Security:** Uses OAuth2PasswordBearer scheme, JWT tokens (via `create_acces_token`, `verify_token`), and password hashing. Database operations use SQLAlchemy ORM with dependency injection.

**Note:** Code appears incomplete (login endpoint unfinished) and has mixed patterns (queries both database and deprecated `users_list`).](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Authentication & Security Module Summary

## Purpose
Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm
- `verify_password()` - Compares plain text password against hashed version

**JWT Authentication:**
- `oauth2_scheme` - OAuth2 security scheme expecting bearer tokens from `/auth/login` endpoint
- `SECRET_KEY` / `ALGORITHM` - Credentials for signing/validating JWT tokens (HS256)

**User Retrieval:**
- `get_user()` - FastAPI dependency that:
  1. Extracts JWT token from request header
  2. Decodes token using SECRET_KEY
  3. Retrieves user email from token payload ("sub" claim)
  4. Queries database for matching user
  5. Returns user object or raises 401 HTTPException if validation fails

## Important Notes
- ⚠️ **Security Issue**: SECRET_KEY is hardcoded as "protected" (should use environment variables)
- Uses SQLAlchemy ORM for database queries
- Includes debug print statements (should be removed in production)](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles JWT token creation and verification for authentication.

**Key Components:**

1. **Configuration Constants:**
   - `SECRET_KEY`: Signing key for JWT tokens
   - `ALGORITHM`: HS256 hashing algorithm
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token TTL (30 minutes default)

2. **`create_acces_token(data, expires_delta)`**
   - Generates JWT access tokens
   - Accepts custom expiration time or uses default
   - Encodes payload with expiration claim (`exp`)
   - Returns encoded token string

3. **`verify_token(token)`**
   - Decodes and validates JWT tokens
   - Returns payload dict if valid
   - Returns `None` if token is invalid/expired (catches JWTError)

**Note:** Function has typo: `create_acces_token` should be `create_access_token`. Also, hardcoded `SECRET_KEY` should be externalized for security.](#\utils\jwthandlerspy)

---


---

