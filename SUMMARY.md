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

**Purpose:** Database configuration and initialization module for a FastAPI gift-tracking application using PostgreSQL.

## Key Components:

1. **Database Connection Setup**
   - Connects to AWS RDS PostgreSQL instance using SQLAlchemy
   - Credentials hardcoded (security risk - should use env variables)

2. **Core Objects**
   - `engine`: Database connection pool
   - `SessionLocal`: Session factory for DB operations
   - `Base`: Declarative base class for ORM models to inherit from

3. **Key Functions**
   - `init_db()`: Creates all database tables defined in ORM models
   - `get_db()`: Dependency injection function that yields a database session and ensures proper cleanup

4. **Mock Data** (for testing/development)
   - `gifts_mock`: Sample gift objects with id, name, brand, price
   - `users_list`: Sample user objects with id, name, email

## Important Notes:
- **Security Issue**: Database credentials are hardcoded in the file (should use environment variables)
- Commented-out Pydantic models suggest this was used for API schema validation
- Uses SQLAlchemy ORM pattern with session management for database operations](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Summary

**Purpose**: Main entry point for a FastAPI backend application called "Gifters" - appears to be a gift management/sharing platform.

**Key Components**:

1. **CORS Configuration**: Sets up cross-origin request handling, allowing requests from `http://localhost:3000` (frontend) with full credential and header support.

2. **Database Initialization**: Calls `init_db()` to set up the database on startup.

3. **Route Registration**: Includes routers for:
   - `gifts` - gift management endpoints
   - `users` - user management endpoints
   - `share` - sharing functionality endpoints
   - `auths` - authentication (currently disabled)

4. **Health Check Endpoint**: GET `/` returns a simple success message to verify the backend is running.

**Key Logic**: Standard FastAPI app setup with middleware configuration and modular route organization. The CORS middleware enables browser-based requests from the frontend while the commented-out auth router suggests authentication features may be in development or not yet integrated.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# Code Summary: Gifters API

## Purpose
FastAPI-based REST API for a gift shopping application with endpoints for greetings, echoing text, searching/listing gifts, and user retrieval.

## Key Components

**Framework & Validation:**
- FastAPI for HTTP server
- Pydantic `BaseModel` for request payload validation (type-safe schemas)

**Core Endpoints:**

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Root health check |
| GET | `/ping` | Status check |
| GET | `/greet/{name}` | Simple greeting with path parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with optional query params (`excited`, `times`) |
| POST | `/echo` | Echo text N times (validates `EchoPayload` schema) |
| GET | `/gifts` | List all gifts (mock data) |
| GET | `/gifts/search` | Filter gifts by optional `brand` and `max_price` query params |
| GET | `/user/{user_id}` | Get user by ID (mock response) |
| GET | `/users/db/{user_id}` | Get user from "database" (incomplete) |

## Important Logic
- **Query filtering** (gifts search): Uses list comprehension with conditional logic to filter by brand and price
- **Optional parameters**: Demonstrates Pydantic's `Optional[T]` for nullable query params
- **Path & query parameters**: Shows FastAPI's automatic type conversion and validation
- **Mock data**: Uses hardcoded dictionaries for testing (no actual DB)

**Note:** Code uses string repetition (`*`), f-strings for templating, and list comprehensions for filtering.](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

## Purpose
Defines SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models

1. **AuthProvider** (Enum)
   - Defines authentication types: `local`, `google`, `guest`, `user`

2. **User**
   - Core user entity with email, name, hashed password
   - Supports multiple auth providers (local, Google OAuth)
   - Relations: owns multiple `Gifts` and `GiftsList` entries
   - Tracks creation timestamp

3. **Gifts**
   - Individual gift items with metadata (name, brand, size, color, price, link, note)
   - `claimed` boolean flag tracks if gift is reserved
   - Foreign key to `User` (owner)
   - One-to-many relationship with User

4. **GiftsList**
   - Container for grouping user's gifts
   - Includes shareable `share_token` (UUID) for list sharing
   - Links User to their gift lists

5. **RefreshTokens**
   - Stores JWT refresh tokens for authenticated sessions
   - Foreign key to User

6. **ExternalUser**
   - Records for OAuth users (Google integration)
   - Stores Google ID, name, email

## Key Logic
- **Relationships**: ORM relationships (`back_populates`) create bidirectional object links without adding DB columns
- **Foreign Keys**: Enforce referential integrity (gifts must belong to valid users)
- **Enums**: Restrict `auth_provider` and `mode` to predefined values
- **UUID Generation**: Share tokens auto-generated for gift list sharing](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Code Summary: Gifters Backend Deployment Guide

## Purpose
This is a **deployment and infrastructure setup guide** for a FastAPI backend application, covering database migration, AWS hosting setup, and production server configuration.

## Key Sections

### 1. **Database Migration (Alembic)**
- Manages schema changes using Alembic
- Commands: `autogenerate`, `upgrade head`, `stamp head`
- Example: Adding hashed password column to users table

### 2. **AWS RDS Database Setup**
- Host PostgreSQL/MySQL database on AWS RDS
- Configure connection URL, port, and credentials for backend

### 3. **AWS EC2 Instance Setup**
- Launch Ubuntu instance on EC2
- Configure **Key Pair** (SSH authentication)
- Configure **Security Groups** (inbound/outbound firewall rules)
- Install dependencies: Python, pip, venv, git, nginx

### 4. **Application Deployment**
- Clone repository
- Create Python virtual environment
- Install dependencies via `pip install -r requirements.txt`
- Run Uvicorn server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### 5. **Production Service (Systemd)**
- Create `/etc/systemd/system/fastapi.service` file
- Configure auto-restart, logging, and 24/7 uptime
- Manage via systemctl commands:
  - `daemon-reload`, `start`, `enable`, `restart`, `status`

## Important Components
- **Uvicorn**: ASGI server running FastAPI app
- **Nginx**: Reverse proxy for production traffic (mentioned but not configured in detail)
- **Systemd**: Linux service manager for persistent](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Code Summary: Pydantic Schemas

**Purpose:** Defines request/response data validation schemas for a gift-sharing application using Pydantic models.

**Key Components:**

1. **User Schemas**
   - `UserCreate`: Registration payload (name, email, password)
   - `UserLogin`: Login credentials (email, password)
   - `UserGuest`: Third-party authentication (email, name, provider_id)
   - `UserResponse`: API response with user data (excludes password); uses `orm_mode` to accept SQLAlchemy objects

2. **Authentication Response**
   - `GuestResponse`: Returns authenticated user + access token

3. **Gift Schemas**
   - `GiftTemplate`: Gift creation model with optional fields (brand, size, color, link, note)
   - `GiftResponse`: Full gift data returned from API (extends template, adds id, user_id, claimed status)
   - `GiftOut`: Minimal gift info for listing (id, claimed status, claimer name)

**Important Details:**
- All response models use `orm_mode = True` to seamlessly convert ORM objects to JSON
- Optional fields use `Optional[str/int]` with sensible defaults (None)
- Inheritance reduces duplication (`GiftResponse` extends `GiftTemplate`)
- Clean separation between input validation and output serialization](#\schemaspy)

---

- [\SUMMARY.md](#\summarymd)
- [I appreciate your request, but I don't have the ability to directly access files on your local machine at `C:\Users\Balaji\Projects\repo_summarizer\gifters-backend_summary.md`.

However, I can help you in a few ways:

1. **Copy and paste the content** - You can paste the file contents directly into our chat, and I'll provide a concise summary
2. **Share the code** - If you paste the code here, I'll focus on:
   - **Purpose** of the file
   - **Key logic** and algorithms
   - **Important functions/components**
   - **Dependencies and integrations**

Please share the code, and I'll give you a brief, focused summary as a senior software engineer would.](#\summarymd)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Marks the containing directory as a Python package, allowing it to be imported as a module
- Currently empty (contains only a comment)
- No functions, classes, or logic are defined

This is a minimal package structure file with no active functionality.](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI web application called "Gifters"

**Key Logic:**
- Creates a FastAPI application instance with the title "Gifters"
- Includes routing configuration from an external `gifts` module

**Important Components:**
- `FastAPI()` - Initializes the web framework
- `app.include_router()` - Registers the gifts router to handle gift-related endpoints

This is a minimal setup file that delegates actual route definitions to a separate `routes/gifts.py` module.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary: Google OAuth Authentication Module

## Purpose
Sets up Google OAuth 2.0 authentication endpoints for a FastAPI application, enabling users to log in via Google and receive JWT tokens.

## Key Components

**OAuth Configuration**
- Registers Google OAuth client with credentials from environment variables
- Sets up Google endpoints for authorization and token exchange
- Defines scopes: `openid email profile`

**Database Dependency**
- `get_db()`: Yields a SQLAlchemy session for database operations, with cleanup

**Commented-Out Endpoints** (Currently disabled)
- `/google/login`: Initiates OAuth flow by redirecting to Google's login
- `/google/callback`: Handles OAuth callback, which:
  - Retrieves and validates Google ID token
  - Checks if user exists in `ExternalUser` table; creates if new
  - Generates JWT token with `user_id`, `email`, and `role` claim
  - Returns bearer token to frontend

## Important Notes
- All authentication logic is currently commented out
- Uses `authlib` for OAuth handling and `PyJWT` for token generation
- Follows FastAPI best practices with dependency injection and routers](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary: Gifts API Router

## Purpose
FastAPI router for managing gift records with CRUD operations, including user authentication and search functionality.

## Key Components

**Pydantic Models** (request/response validation):
- `GiftCreate`: Base model for gift creation (name, brand, size, color)
- `GiftPatch`: Optional fields for partial updates
- `Gift`: Extends GiftCreate with an id field

**Database Functions**:
- `get_db()`: Dependency that provides SQLAlchemy session management with proper cleanup

**Endpoints**:

1. **GET `/fetch/{user_id}`** - Fetches all gifts for a user
   - Requires JWT token in Authorization header
   - Validates token before returning gifts
   - Returns 404 if user has no gifts, 401 if unauthorized

2. **GET `/searchby/{column}/{value}`** - Searches gifts by any column
   - Validates column names against allowlist (id, name, brand, size, color, user_id)
   - Case-insensitive search with whitespace trimming
   - Uses `getattr()` for dynamic attribute access

3. **POST `/add/{user_id}`** - Creates a new gift (incomplete in snippet)
   - Expects authorization header

## Important Logic
- Token verification via `verify_token()` before returning user data
- SQL injection prevention through allowlist validation on dynamic queries
- Case-insensitive, whitespace-tolerant search filtering using SQLAlchemy's `func.lower()`](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Code Summary

**Purpose:** FastAPI router for creating and retrieving shareable gift list links.

**Key Logic:**
- Creates unique shareable URLs for gift lists
- Retrieves gift items associated with a shared token

**Important Functions:**

1. **`create_sharable_links(user_id)`** - POST endpoint
   - Creates a new `GiftsList` record for the user
   - Generates a unique `share_token` (auto-generated by model)
   - Returns a shareable URL with the token
   - Includes error handling for database failures

2. **`get_gifts(token)`** - GET endpoint
   - Validates the share token exists
   - Retrieves all gifts belonging to the list owner
   - Returns owner ID and their gift list
   - Raises 401 error if token is invalid

**Database:** Uses SQLAlchemy ORM with models `GiftsList` and `Gifts`](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# User Authentication & Management API Router

## Purpose
FastAPI router handling user authentication, registration, and user management with JWT-based security.

## Key Components

**Authentication:**
- `get_current_user()` - Dependency that validates JWT tokens and returns authenticated user from database
- Uses OAuth2 Bearer token scheme
- Decodes JWT and queries database for user verification

**Endpoints:**
- `POST /users/register` - User registration with password hashing and duplicate email validation
- `POST /users/login/basic` - (incomplete) Basic login endpoint
- `POST /users/post` - Create new user directly
- `GET /users/search/{id}` - Fetch user by ID

**Security:**
- Password hashing via `hash_password()` utility
- JWT token creation/verification using `create_acces_token()` and `verify_token()`
- Token validation in `get_current_user()` dependency

**Database:**
- Uses SQLAlchemy ORM with `Session` dependency injection
- Stores `User` and `RefreshTokens` models
- Email uniqueness enforced in registration

## Issues
- Code is incomplete (login endpoint cut off)
- Some debug print statements left in register function
- Mixed logic referencing unused `users_list` variable
- Inconsistent error handling (one uses `return` instead of `raise`)](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Security & Authentication Module Summary

## Purpose
Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

## Key Components

**Password Management:**
- `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm
- `verify_password()` - Validates plain text password against hashed version

**JWT Authentication:**
- `oauth2_scheme` - OAuth2 bearer token extractor from requests
- `SECRET_KEY` & `ALGORITHM` - JWT signing credentials (HS256)

**Core Logic:**
- `get_user()` - Dependency function that:
  1. Extracts JWT token from request header (via OAuth2PasswordBearer)
  2. Decodes token and retrieves email from "sub" claim
  3. Queries database for matching user
  4. Returns user object or raises 401 HTTPException on failure

## Important Notes
- Uses Passlib's automatic deprecation system to support future algorithm upgrades
- Returns credentials error (401) for invalid/missing tokens or non-existent users
- Designed as FastAPI dependency for route protection via `Depends(get_user)`](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Authentication Module

**Purpose:** Handles JWT token creation and verification for authentication/authorization.

**Key Components:**

1. **Configuration Constants:**
   - `SECRET_KEY`: Signing key for JWT tokens (hardcoded - security risk)
   - `ALGORITHM`: HS256 (HMAC SHA-256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30-minute default expiration

2. **`create_acces_token()`** - Creates signed JWT tokens
   - Accepts data dict and optional expiration delta
   - Adds `exp` claim with UTC timestamp
   - Returns encoded JWT string

3. **`verify_token()`** - Validates and decodes JWT tokens
   - Decodes token using secret key
   - Returns payload on success, `None` on JWTError (invalid/expired token)

**Note:** Uses `jose` library for JWT operations with UTC timezone awareness.](#\utils\jwthandlerspy)

---


---

