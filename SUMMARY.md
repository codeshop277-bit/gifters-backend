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

**Purpose:** Sets up SQLAlchemy database connection and session factory for a PostgreSQL database on AWS RDS.

**Key Components:**

1. **Database Connection**
   - `DATABASE_URL`: PostgreSQL connection string to AWS RDS instance (gifters database)
   - `engine`: Core database connection interface

2. **Session Management**
   - `SessionLocal`: Factory for creating ORM sessions (`autocommit=False, autoflush=False`)
   - `db`: Active session instance for DB operations

3. **ORM Base Class**
   - `Base`: Declarative base that all SQLAlchemy models inherit from for automatic table mapping

4. **Key Functions**
   - `init_db()`: Creates all tables defined in models (calls `Base.metadata.create_all()`)
   - `get_db()`: Generator function that provides a session for dependency injection in FastAPI routes; ensures proper session cleanup

**Security Note:** Database credentials are hardcoded (should use environment variables instead).](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary

**Purpose**: Main entry point for a FastAPI application called "Gifters" - appears to be a gift management/sharing backend service.

**Key Setup**:
- **CORS Configuration**: Enables cross-origin requests from `localhost:3000` with full method/header flexibility and credential support
- **Database**: Initializes database connection via `init_db()`
- **Route Registration**: Mounts routers for gifts, users, and share functionality (auth router commented out)

**Main Components**:
- `app = FastAPI(title="Gifters")` - Core FastAPI application
- `CORSMiddleware` - Handles cross-origin requests from frontend
- Route includes: `/gifts`, `/users`, `/share` endpoints
- Root endpoint `GET /` - Health check returning a success message

**Note**: The auth router is currently disabled, suggesting authentication features may be under development.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
A FastAPI-based REST API for a gift management system with endpoints for greeting users, echoing text, and searching/listing gifts.

## Key Components

**Framework & Setup:**
- FastAPI application with title "Gifters API"
- Uses Pydantic `BaseModel` for request validation
- Supports both query parameters and path parameters

**Main Endpoints:**

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Health check - returns welcome message |
| GET | `/ping` | Status check |
| GET | `/greet/{name}` | Basic greeting with name parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with optional `excited` (bool) and `times` (int) query params |
| POST | `/echo` | Echoes text based on `EchoPayload` - repeats string N times |
| GET | `/gifts` | Returns mock list of gifts |
| GET | `/gifts/search` | Filters gifts by optional `brand` and `max_price` query params |
| GET | `/user/{user_id}` | Returns mock user by ID |
| GET | `/users/db/{user_id}` | Returns mock user from "database" |

**Key Logic:**
- **Path parameters**: Dynamic routing (e.g., `/greet/{name}`)
- **Query parameters**: Optional filtering (brand, max_price, excited, times)
- **Data validation**: Uses `EchoPayload` Pydantic model for POST requests
- **List filtering**: `/gifts/search` uses list comprehension with conditional filters
- **Mock data**: All endpoints return hardcoded test data (no real database](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
SQLAlchemy ORM model definitions for a gift-sharing application with user authentication and gift list management.

## Key Models

**User** - Core user entity with:
- Email-based authentication (unique constraint)
- Support for multiple auth providers (local, Google, guest)
- One-to-many relationship with Gifts and GiftsList
- Timestamps for account creation

**Gifts** - Gift items owned by users with:
- Product details (name, brand, size, color, price, link)
- Claim status (boolean flag)
- Foreign key to User (owner)
- Optional notes and claimer relationship

**GiftsList** - Shareable gift collections with:
- Unique `share_token` (UUID) for public sharing
- User ownership via foreign key
- Timestamp tracking

**Supporting Models**:
- **AuthProvider** enum - Supports local, Google OAuth, guest, and user modes
- **RefreshTokens** - JWT token management for authenticated sessions
- **ExternalUser** - OAuth user data storage (Google integration)

## Important Features
- Relationships use `back_populates` for bidirectional ORM linking (e.g., user.gifts and gift.owner)
- Timestamp defaults to UTC for consistency
- Unique constraints on email, tokens, and OAuth IDs for data integrity
- Foreign key constraints ensure referential integrity](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Code Summary: Gifters Backend Deployment Guide

## Purpose
This is a **deployment and setup documentation** (not executable code) for a FastAPI backend application, covering database migrations, AWS hosting setup, and production service configuration.

## Key Sections

### 1. **Database Migrations (Alembic)**
- Uses Alembic to manage schema changes
- Commands to auto-generate and apply migrations (e.g., adding hashed password columns)

### 2. **AWS Infrastructure Setup**
- **RDS**: Host PostgreSQL/MySQL database in AWS
- **EC2**: Host backend application on virtual machine instances
- **Security Configuration**: 
  - Key pairs for SSH authentication
  - Security groups to control inbound/outbound traffic

### 3. **EC2 Instance Setup**
- Install dependencies: Python, pip, venv, git, nginx
- Clone repository and create isolated Python virtual environment
- Install project dependencies via `requirements.txt`
- Test run with: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 4. **Production Service (Systemd)**
- Creates a systemd service file to run FastAPI application 24/7
- Auto-restart on failure (RestartSec=3)
- Runs Uvicorn as Ubuntu user on port 8000
- Enable/start service with systemctl commands

## Important Commands
| Purpose | Command |
|---------|---------|
| Apply migrations | `alembic upgrade head` |
| Connect to EC2 | `ssh -i key.pem ubuntu@IP` |
| Run app locally | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| Start service](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Code Summary: Pydantic Schemas

**Purpose:** Defines data validation and serialization schemas for a gift-sharing application using Pydantic models.

**Key Components:**

1. **User Schemas:**
   - `UserCreate` - Registration input (name, email, password)
   - `UserLogin` - Authentication input (email, password)
   - `UserGuest` - OAuth/guest user input (email, name, provider_id)
   - `UserResponse` - User output with ORM mode enabled for SQLAlchemy object conversion

2. **Authentication:**
   - `GuestResponse` - Combines user data + access token for login responses

3. **Gift Schemas:**
   - `GiftTemplate` - Base gift creation schema with optional fields (brand, size, color, link, note, price)
   - `GiftResponse` - Extended template with database fields (id, user_id, claimed status) and ORM mode
   - `GiftOut` - Minimal gift summary for listing (id, claimed status, claimed_by user)

**Important Details:**
- All schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to Pydantic models
- Optional fields use `Optional[str/int]` for flexible data submission
- Separates input validation (Create/Login) from output serialization (Response models)](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Marks the containing directory as a Python package, allowing it to be imported as a module
- Currently empty (or nearly empty) - no initialization logic or imports are defined
- Enables the directory structure to be recognized by Python's import system

**Typical Use:** This file exists in package directories to allow `from package import module` style imports to work correctly.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Entry point for a FastAPI application called "Gifters"

**Key Components:**
- Creates a FastAPI application instance with the title "Gifters"
- Includes routing from a `gifts` module to handle gift-related endpoints

**Functionality:** This is a minimal main application file that initializes the FastAPI server and registers the gifts router, which presumably handles gift-related API operations.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary

**Purpose:** FastAPI authentication module for Google OAuth 2.0 integration with JWT token generation.

**Key Components:**

1. **OAuth Configuration** - Registers Google as OAuth provider with credentials from environment variables
   - Configures Google's OAuth endpoints and scopes (openid, email, profile)

2. **Database Helper** - `get_db()` dependency that provides SQLAlchemy session management with automatic cleanup

3. **Commented Implementation** - Contains disabled OAuth callback flow that would:
   - Exchange Google auth code for access token
   - Parse user info from ID token
   - Create/retrieve `ExternalUser` from database
   - Generate JWT token with user claims (user_id, email, role)
   - Return bearer token to frontend

**Current State:** OAuth client is configured but login/callback endpoints are commented out, suggesting this is work-in-progress or the flow is handled elsewhere.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Gifts API Router Summary

**Purpose:** FastAPI router that manages gift CRUD operations with JWT authentication and database persistence.

## Key Components:

**Pydantic Models:**
- `GiftCreate` - Request payload for creating gifts (name, brand, size, color)
- `GiftPatch` - Optional fields for updates
- `Gift` - GiftCreate + id field
- `GiftResponse` - Database response schema

**Database Setup:**
- `get_db()` - Dependency that yields SQLAlchemy Session and ensures cleanup

## Endpoints:

1. **`GET /gifts/fetch/{user_id}`**
   - Retrieves all gifts for a user
   - Validates JWT token from Authorization header
   - Returns `List[GiftResponse]`
   - Raises 401 if token missing/invalid, 404 if user not found

2. **`GET /gifts/searchby/{column}/{value}`**
   - Searches gifts by dynamic column (id, name, brand, size, color, user_id)
   - Case-insensitive search with whitespace trimming
   - Validates column exists before querying
   - Returns matching results or 404

3. **`POST /gifts/add/{user_id}`** (incomplete)
   - Creates new gift for user
   - Requires Authorization header
   - Uses `GiftTemplate` schema

**Key Logic:**
- Dynamic column filtering via `getattr()` for flexible searches
- JWT token extraction from "Bearer {token}" format
- Case-insensitive database queries using SQLAlchemy `func.lower()`
- Authentication validation on protected endpoints](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Code Summary

**Purpose:** FastAPI router for creating and retrieving shareable gift lists via token-based links.

**Key Logic:**
- Generates unique shareable URLs for gift lists
- Validates share tokens and retrieves associated gifts

**Main Endpoints:**

1. **`POST /{user_id}`** - `create_sharable_links()`
   - Creates a new `GiftsList` record for a user
   - Returns a shareable URL with an auto-generated `share_token`
   - Handles database errors with rollback on `SQLAlchemyError`

2. **`GET /token/{token}`** - `get_gifts()`
   - Validates the share token against the database
   - Retrieves all gifts belonging to the list owner
   - Returns owner ID and associated gift objects
   - Raises 401 error if token is invalid

**Dependencies:** FastAPI, SQLAlchemy ORM, custom database and model modules](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# User Authentication & Management API Router

## Purpose
FastAPI router that handles user authentication (registration, login) and user management operations with JWT-based token verification.

## Key Components

**Authentication:**
- `get_current_user()`: Dependency that validates JWT tokens, decodes them, and retrieves the authenticated user from the database
- OAuth2 password bearer scheme for token extraction from requests
- JWT token validation with error handling for expired/invalid tokens

**Endpoints:**

1. **`/search/{id}`** (GET) - Fetches a user by ID
2. **`/post`** (POST) - Creates a new user directly from UserCreate data
3. **`/register`** (POST) - User registration with:
   - Email uniqueness validation
   - Password hashing using `hash_password()`
   - New user creation and storage in database
4. **`/login/basic`** (POST) - *Incomplete* (function cut off)

**Key Logic:**
- Password security: Hashes passwords before storage
- Database operations: Uses SQLAlchemy ORM with dependency injection for DB sessions
- Token handling: Decodes JWT payloads to extract user ID and verify token validity
- Error handling: Raises 401 (unauthorized) and 404 (not found) exceptions appropriately

**Dependencies:**
- SQLAlchemy for database queries
- JWT for token encoding/decoding
- Bcrypt-based password hashing utilities

*Note: The login endpoint is incomplete, and there's some unused/commented code (like `users_list` reference).*](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Code Summary: Authentication & Authorization Module

## Purpose
Handles secure password hashing and JWT token-based authentication for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256
- `verify_password()` - Validates plain text password against stored hash

**JWT Authentication:**
- `oauth2_scheme` - OAuth2 bearer token extractor for API endpoints
- `SECRET_KEY` & `ALGORITHM` - JWT signing credentials (HS256)

**Core Logic - `get_user()`**
- Dependency function that validates JWT tokens from request headers
- Decodes JWT payload to extract email ("sub" claim)
- Queries database for matching user record
- Returns authenticated `User` object or raises 401 HTTPException on failure
- Handles JWT decode errors gracefully with exception handling

## Important Notes
- Uses Passlib's auto-deprecation to support future algorithm migrations
- Integrates with FastAPI's dependency injection system (`Depends`)
- ⚠️ **Security Issue**: SECRET_KEY hardcoded as "protected" (should use environment variables)
- Debug print statements present (should be removed in production)](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Management Module

**Purpose:** Handles authentication token creation and validation for a FastAPI/web application.

**Key Components:**

1. **Configuration Constants:**
   - `SECRET_KEY`: Signing key for JWT tokens (should be environment variable, not hardcoded)
   - `ALGORITHM`: HS256 for HMAC-based token signing
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30-minute token lifetime

2. **`create_acces_token()`** *(note: typo in function name)*
   - Creates JWT tokens with custom or default expiration
   - Adds `exp` claim for token expiration
   - Returns encoded JWT string

3. **`verify_token()`**
   - Decodes and validates JWT tokens
   - Returns payload dict if valid, `None` if invalid/expired
   - Catches JWT-related errors gracefully

**⚠️ Security Notes:**
- SECRET_KEY is hardcoded (should use environment variables)
- No user/claim validation beyond JWT signature check
- Function name has typo: `create_acces_token` → `create_access_token`](#\utils\jwthandlerspy)

---


---

