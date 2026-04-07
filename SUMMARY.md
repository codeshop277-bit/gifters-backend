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

# Database Configuration & Setup

**Purpose:** Initializes SQLAlchemy database connection and session management for a PostgreSQL database.

**Key Components:**

1. **Database Connection**
   - Connects to AWS RDS PostgreSQL instance using credentials and connection string
   - Creates `engine` (core DB interface) via `create_engine()`

2. **Session Factory**
   - `SessionLocal` = factory for creating ORM sessions
   - `get_db()` = dependency injection function that yields a session and safely closes it (useful for FastAPI)

3. **ORM Base**
   - `Base = declarative_base()` = metaclass for all SQLAlchemy models to inherit from
   - Enables automatic table mapping

4. **Database Initialization**
   - `init_db()` = creates all tables defined in models that inherit from `Base`

**Important Functions:**
- `get_db()` - FastAPI dependency for injecting DB sessions into routes
- `init_db()` - Initializes schema on app startup

⚠️ **Security Note:** Database credentials are hardcoded; should use environment variables instead.

---

### `\main.py`

# Code Summary: FastAPI Backend Application

**Purpose:** Main entry point for a "Gifters" backend API application that manages gifts, users, and sharing functionality.

**Key Setup:**
- **CORS Configuration**: Enables cross-origin requests from `localhost:3000` (frontend), allowing credentials and all HTTP methods/headers
- **Database Initialization**: Calls `init_db()` to set up the database connection
- **Router Registration**: Integrates route modules for:
  - `gifts` - Gift management endpoints
  - `users` - User management endpoints
  - `share` - Sharing functionality endpoints
  - `auths` - Authentication (currently disabled/commented out)

**Important Components:**
- `app` - FastAPI application instance
- `@app.get("/")` - Health check endpoint returning a success message

**Architecture:** Standard FastAPI setup with modular routing, middleware for CORS handling, and database initialization on startup.

---

### `\mainlearn.py`

# Code Summary: Gifters API

## Purpose
A FastAPI-based REST API for a gift management system with endpoints for greeting users, searching/listing gifts, and user retrieval.

## Key Components

**Framework & Validation:**
- FastAPI for HTTP routing and automatic OpenAPI documentation
- Pydantic `BaseModel` for request payload validation (e.g., `EchoPayload`)

**Core Endpoints:**

| Method | Route | Function |
|--------|-------|----------|
| GET | `/` | Root welcome message |
| GET | `/ping` | Health check |
| GET | `/greet/{name}` | Simple greeting with path parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with optional query params (`excited`, `times`) |
| POST | `/echo` | Echoes text with repetition (validates `EchoPayload`) |
| GET | `/gifts` | Lists all gifts (mock data) |
| GET | `/gifts/search` | Filters gifts by optional `brand` and `max_price` query params |
| GET | `/user/{user_id}` | Retrieves single user by ID |
| GET | `/users/db/{user_id}` | Retrieves user from mock database |

## Important Patterns
- **Path parameters** (e.g., `{name}`, `{user_id}`) are extracted from URL
- **Query parameters** (e.g., `excited`, `times`, `brand`, `max_price`) use `Optional[Type]` for non-required fields
- **Mock data** hardcoded in endpoints (no real database)
- **Filtering logic** uses list comprehension to filter gifts based on multiple optional criteria

---

### `\models.py`

# Code Summary

## Purpose
SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models

1. **User** - Central entity with authentication support
   - Email, hashed password, name
   - Multiple auth providers (local, Google, guest)
   - One-to-many relationships with Gifts and GiftsList

2. **Gifts** - Gift items that users create/own
   - Properties: name, brand, size, color, link, price, note
   - `claimed` boolean flag to track gift status
   - Foreign key to User (owner)

3. **GiftsList** - Shareable gift collection
   - Unique `share_token` (UUID) for sharing lists
   - Links users to their curated gift lists

4. **RefreshTokens** - JWT token management
   - Stores refresh tokens per user for session handling

5. **ExternalUser** - OAuth user tracking
   - Stores Google authentication details separately

## Key Features
- **Enum-based auth**: AuthProvider restricts authentication methods
- **Relationships**: Bidirectional ORM relationships (User ↔ Gifts, User ↔ GiftsList)
- **Timestamps**: Auto-generated UTC creation dates
- **Claim tracking**: Gifts can be marked as claimed with potential claimer relationship
- **Token-based sharing**: GiftsList uses UUID tokens for secure sharing

---

### `\README.md`

# Summary

This is **documentation/setup guide** for a FastAPI backend project called "gifters-backend," not actual code. It covers:

## Key Sections:

1. **Database Migrations** - Using Alembic to manage schema changes (adding columns, versioning)

2. **AWS RDS Setup** - Instructions to host PostgreSQL/database in AWS with connection details

3. **AWS EC2 Deployment** - Steps to launch and configure a Linux instance:
   - Security groups (firewall rules for inbound/outbound traffic)
   - Install dependencies (Python, pip, venv, git, nginx)
   - Clone repository and create isolated Python environment

4. **Running the Application** - Start FastAPI with Uvicorn on port 8000

5. **Production 24/7 Service** - Creates systemd service file to:
   - Auto-start Uvicorn on server boot
   - Auto-restart on failures
   - Run as ubuntu user with proper environment

## Important Commands:
- `alembic upgrade head` - Apply database migrations
- `python3 -m venv venv` - Create isolated environment
- `sudo systemctl enable fastapi` - Enable auto-start on boot

**Purpose**: Complete deployment guide for taking a FastAPI backend from local development to production on AWS infrastructure.

---

### `\schemas.py`

# Summary: Pydantic Schemas for User and Gift Management

**Purpose**: Defines request/response validation schemas for a gift-sharing application with user authentication and guest support.

**Key Components**:

1. **User Schemas**:
   - `UserCreate`: Registration payload (name, email, password)
   - `UserLogin`: Login credentials (email, password)
   - `UserGuest`: OAuth/guest user creation (email, name, provider_id)
   - `UserResponse`: User data output with ORM mode enabled for SQLAlchemy compatibility

2. **Authentication Response**:
   - `GuestResponse`: Returns authenticated user + JWT access token

3. **Gift Schemas**:
   - `GiftTemplate`: Base gift creation model with optional fields (brand, size, color, link, note, price)
   - `GiftResponse`: Full gift object with additional tracking (id, user_id, claimed status) - inherits from GiftTemplate
   - `GiftOut`: Minimal gift view (id, claimed status, and who claimed it)

**Important Details**:
- All response schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to Pydantic models
- Uses `Optional` fields for flexible gift attributes
- Price stored as `int` (likely cents to avoid float precision issues)

---

### `\__init__.py`

# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Empty or minimal file that marks the containing directory as a Python package
- Allows the directory to be imported as a module
- Enables the use of relative imports within the package

**No significant logic or functions** - this is a standard package marker file.

---

### `\app\main.py`

# Code Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters"

**Key Components:**
- Creates a FastAPI application instance with the title "Gifters"
- Includes a router from the `routes.gifts` module to handle gift-related API endpoints

**Functionality:** This is a minimal setup file that initializes the web application and registers routing logic, delegating the actual endpoint definitions to a separate `gifts` router module.

---

### `\routes\auths.py`

# Summary: Google OAuth Authentication Module

## Purpose
This file sets up Google OAuth 2.0 authentication for a FastAPI application, with infrastructure to handle user login and registration via Google.

## Key Components

**OAuth Configuration:**
- Registers Google as an OAuth provider using Authlib
- Configures client credentials (ID/secret) from environment variables
- Sets up Google's OAuth endpoints and requested scopes (openid, email, profile)

**Database Dependency:**
- `get_db()` function provides SQLAlchemy session management for database operations

**Commented Implementation:**
The file contains disabled endpoint stubs for the complete OAuth flow:
- **`/google/login`** - Redirects users to Google's login page
- **`/google/callback`** - Handles OAuth callback with logic to:
  - Parse Google's ID token
  - Extract user info (email, name, Google ID)
  - Create or retrieve `ExternalUser` from database
  - Generate JWT token for session management
  - Return access token to frontend

## Key Logic
- User lookup/creation based on Google ID
- JWT token generation using HS256 algorithm with user context (ID, email, role)
- Database transaction handling for new user registration

**Status:** The OAuth endpoints are currently disabled (commented out), likely pending frontend integration or further development.

---

### `\routes\gifts.py`

# FastAPI Gifts Router Summary

## Purpose
REST API router for managing gift records, providing endpoints to fetch, search, and add gifts with JWT authentication and database persistence.

## Key Components

### Pydantic Models
- **GiftCreate**: Input model for creating gifts (name, brand, size, color)
- **Gift**: Extends GiftCreate with id field
- **GiftPatch**: Optional fields for partial updates
- **GiftResponse/GiftTemplate**: Schema models for API responses

### Database
- Uses SQLAlchemy ORM with `SessionLocal()` for database connections
- `get_db()` dependency manages session lifecycle (yields connection, closes on completion)

### Endpoints

1. **GET `/fetch/{user_id}`**
   - Retrieves all gifts for a specific user
   - Requires JWT token in Authorization header (Bearer format)
   - Validates token before returning gifts
   - Returns 401 if missing/invalid token, 404 if user not found

2. **GET `/searchby/{column}/{value}`**
   - Dynamic column-based search (whitelist: id, name, brand, size, color, user_id)
   - Case-insensitive matching with `func.lower()` and `.strip()`
   - Uses `getattr()` for dynamic attribute access
   - Returns 404 if column invalid or no results found

3. **POST `/add/{user_id}`** (incomplete in provided code)
   - Adds a new gift for user
   - Expects GiftTemplate in request body
   - Requires Authorization header

## Key Logic
- JWT authentication via `verify_token()` 
- SQLAlchemy filtering and queries
- Input validation and error handling with HTTPExceptions
- Dynamic column selection with

---

### `\routes\share.py`

# Code Summary

**Purpose**: FastAPI router for managing shareable gift list links. Allows users to create unique share tokens and retrieve gift lists via those tokens.

**Key Logic**:
- Creates shareable URLs for gift lists by generating a new `GiftsList` record (which auto-generates a `share_token`)
- Retrieves gifts for a specific user by validating the share token

**Important Functions**:

1. **`create_sharable_links(user_id)`** - POST `/share/{user_id}`
   - Creates a new gift list for the user
   - Returns a shareable URL with auto-generated token
   - Handles database errors with rollback

2. **`get_gifts(token)`** - GET `/share/token/{token}`
   - Validates the share token exists
   - Retrieves all gifts belonging to the list owner
   - Returns owner ID and gifts list
   - Raises 401 error if token is invalid

**Dependencies**: SQLAlchemy ORM, FastAPI error handling, database session injection

---

### `\routes\users.py`

# User Management & Authentication API Router

## Purpose
FastAPI router handling user authentication and management endpoints with JWT token-based security.

## Key Logic

**Authentication Flow:**
- `get_current_user()`: Dependency that validates JWT tokens from requests, decodes payload to extract user ID, queries database for user, and raises 401 on invalid/expired tokens

**Core Endpoints:**

1. **`/search/{id}`** (GET) - Fetch user by ID from database
2. **`/post`** (POST) - Create new user without validation
3. **`/register`** (POST) - User registration with:
   - Email uniqueness check
   - Password hashing via `hash_password()`
   - User creation in database
4. **`/login/basic`** (POST) - *Incomplete in provided code*

## Key Components

- **Dependencies**: `get_db` (database session), `oauth2_scheme` (OAuth2 Bearer token)
- **Models**: `User`, `RefreshTokens` (SQLAlchemy)
- **Schemas**: `UserCreate`, `UserResponse`, `UserLogin`, `UserGuest`, `GuestResponse` (Pydantic)
- **Security**: JWT token creation/verification, password hashing/verification
- **Router prefix**: `/users`

## Notable Issues
- Incomplete `/login/basic` endpoint
- Unused `users_list` and `result` variable in search function
- Commented-out alternative token verification logic
- Stores plain password in database despite hashing

---

### `\utils\auth.py`

# Summary: Authentication & Password Management Module

## Purpose
Provides JWT-based authentication and password hashing utilities for a FastAPI application.

## Key Components

**Password Hashing:**
- `hash_password()` - Securely hashes passwords using bcrypt_sha256
- `verify_password()` - Compares plain text password against stored hash
- Uses Passlib's CryptContext for automatic algorithm upgrades

**JWT Authentication:**
- `oauth2_scheme` - OAuth2 Bearer token extractor for API endpoints
- `get_user()` - Dependency function that validates JWT tokens and retrieves authenticated user from database
  - Decodes JWT using HS256 algorithm and SECRET_KEY
  - Extracts user email from token payload ("sub" claim)
  - Queries database for matching user
  - Returns 401 HTTPException on invalid/expired tokens or missing user

## Security Notes
- ⚠️ SECRET_KEY hardcoded as "protected" (should use environment variables)
- Uses standard FastAPI Depends for injection of token and database session
- Includes debug print statements (should be removed in production)

---

### `\utils\jwt_handlers.py`

# JWT Token Management Module

**Purpose:** Handles JWT (JSON Web Token) creation and verification for authentication.

**Key Components:**

1. **Constants:**
   - `SECRET_KEY`: Signing key for tokens
   - `ALGORITHM`: HS256 (HMAC SHA-256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Default token validity (30 min)

2. **`create_acces_token(data, expires_delta)`** - Generates JWT tokens
   - Copies input data and adds expiration claim (`exp`)
   - Uses custom expiration duration or defaults to 30 minutes
   - Returns encoded JWT string

3. **`verify_token(token)`** - Validates JWT tokens
   - Decodes token using secret key and algorithm
   - Returns payload if valid
   - Returns `None` on any JWT error (expired, invalid signature, malformed)

**Note:** Secret key is hardcoded (security concern for production).

---

