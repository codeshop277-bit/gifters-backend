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
Database configuration and initialization file for a FastAPI/SQLAlchemy application connecting to an AWS RDS PostgreSQL database.

## Key Components

**Database Connection:**
- Establishes PostgreSQL connection to AWS RDS using credentials and connection string (`DATABASE_URL`)
- Creates SQLAlchemy `engine` for database communication

**Session Management:**
- `SessionLocal`: Factory for creating database sessions
- `get_db()`: Dependency injection function that yields a session and ensures proper cleanup (close on completion)

**ORM Setup:**
- `Base`: Declarative base class for all SQLAlchemy models to inherit from
- `init_db()`: Creates all database tables defined in models

**Mock Data:**
- `gifts_mock`: List of sample gift objects (id, name, brand, price)
- `users_list`: List of sample user objects (id, name, email)

## Important Notes
⚠️ **Security Issue**: Database credentials are hardcoded in the file—should use environment variables instead.](#\databasepy)

---

- [\main.py](#\mainpy)
- [# Code Summary

**Purpose**: FastAPI application entry point for a "Gifters" backend service - a gift management API.

**Key Setup**:
- **CORS Configuration**: Allows cross-origin requests from `localhost:3000` with credentials and all HTTP methods/headers
- **Database Initialization**: Calls `init_db()` to set up database connections
- **Router Registration**: Includes routes for gifts, users, and share functionality (auths currently disabled)

**Main Components**:
- `FastAPI(title="Gifters")` - Creates the API instance
- `CORSMiddleware` - Handles cross-origin request validation
- Route modules imported: `gifts`, `users`, `auths`, `share`
- Health check endpoint at root (`GET /`) returning success message

**Note**: This is a typical FastAPI scaffold for a gift-sharing application with basic CORS setup for frontend integration.](#\mainpy)

---

- [\mainlearn.py](#\mainlearnpy)
- [# FastAPI Gifters API - Code Summary

## Purpose
A RESTful API built with **FastAPI** for managing gift-related operations (searching, listing gifts) and user management. It demonstrates basic API patterns including path parameters, query parameters, request body validation, and mock data.

## Key Components

### Core Setup
- **FastAPI app** with title "Gifters API" v0.1
- **Pydantic BaseModel** (`EchoPayload`) for request body validation and type safety

### API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Root greeting |
| GET | `/ping` | Health check |
| GET | `/greet/{name}` | Simple greeting with path parameter |
| GET | `/greet-adv/{name}` | Advanced greeting with optional query params (excited, times) |
| POST | `/echo` | Echoes text payload with optional repetition |
| GET | `/gifts` | Returns mock gift list |
| GET | `/gifts/search` | Filters gifts by optional `brand` and `max_price` query params |
| GET | `/user/{user_id}` | Returns mock user by ID |
| GET | `/users/db/{user_id}` | Retrieves user from mock database (incomplete) |

## Important Logic
- **Query parameter filtering** (gifts_search): Uses list comprehension to filter mock data based on optional conditions
- **Type validation**: Path params (`user_id: int`), query params with defaults (`excited: bool = False`), and optional fields (`Optional[str]`)
- **Request body validation**: `EchoPayload` enforces payload structure with required `text` and optional `repeat` fields

## Notes](#\mainlearnpy)

---

- [\models.py](#\modelspy)
- [# Code Summary

**Purpose:** SQLAlchemy ORM models for a gift-sharing application with user authentication and gift list management.

## Key Models:

1. **User** - Core user entity
   - Supports multiple auth providers (local, Google, guest)
   - Stores email, hashed password, name, creation timestamp
   - One-to-many relationship with Gifts and GiftsList

2. **Gifts** - Individual gift items
   - Properties: name, brand, size, color, price, link, notes
   - `claimed` boolean flag to track if someone claimed the gift
   - Foreign key to User (owner) with back_populates relationship

3. **GiftsList** - Gift list collections
   - Belongs to a User
   - Includes `share_token` (UUID) for sharing lists publicly
   - Links gifts to organized lists

4. **RefreshTokens** - JWT token storage
   - Stores refresh tokens per user for session management

5. **ExternalUser** - OAuth user data
   - Tracks Google OAuth users separately (ID, email, name)

## Important Features:
- **Enum validation** for `auth_provider` and `mode` fields
- **Relationships** enable ORM navigation (User→Gifts, GiftsList→User)
- **Unique constraints** on email, tokens, and OAuth IDs
- **UUID generation** for secure gift list sharing tokens
- **Timestamps** for audit trails (created_at)](#\modelspy)

---

- [\README.md](#\readmemd)
- [# Code Summary

## Purpose
This is a **deployment and setup guide** for a FastAPI backend application (`gifters-backend`), not actual source code. It documents the complete infrastructure setup process.

## Key Sections

### 1. **Database Management (Alembic)**
- Commands to create and apply database migrations
- Adds new columns to existing tables (e.g., hashed password to users)
- Uses Alembic for version control of database schema changes

### 2. **AWS RDS Setup**
- Host PostgreSQL/MySQL database on AWS RDS
- Retrieve connection credentials (host, port, credentials)
- Connect backend to remote database

### 3. **AWS EC2 Deployment**
- Launch an Ubuntu EC2 instance
- Configure **Key Pairs** (SSH authentication)
- Configure **Security Groups** (firewall rules - inbound/outbound traffic)
- Connect via SSH and install dependencies (Python, pip, venv, git, nginx)

### 4. **Backend Deployment**
- Clone repository on EC2
- Create isolated Python virtual environment
- Install dependencies from `requirements.txt`
- Run FastAPI with Uvicorn on port 8000

### 5. **Production Service (systemd)**
- Create a systemd service file to run Uvicorn automatically
- Auto-restart on failure
- Enable service to run on server startup (24/7 availability)
- Commands: `daemon-reload`, `start`, `enable`, `restart`, `status`

## TL;DR
Complete guide to deploy a FastAPI backend on AWS EC2 with database on RDS, with automatic service management for continuous operation.](#\readmemd)

---

- [\schemas.py](#\schemaspy)
- [# Summary: schemas.py

## Purpose
Defines Pydantic validation schemas for API request/response serialization in a gift registry application with user authentication.

## Key Components

**User Management**
- `UserCreate`: Registration schema (name, email, password)
- `UserLogin`: Login credentials (email, password)
- `UserGuest`: OAuth/guest user creation (email, name, provider_id)
- `UserResponse`: User output schema with ORM mode enabled for SQLAlchemy compatibility

**Authentication**
- `GuestResponse`: Wraps user data + JWT access token for login responses

**Gift Registry**
- `GiftTemplate`: Base gift model with optional fields (brand, size, color, link, note, price)
- `GiftResponse`: Full gift object returned from DB (extends GiftTemplate, adds id, user_id, claimed status)
- `GiftOut`: Minimal gift view showing only id, claimed status, and who claimed it

## Important Details
- All response schemas use `orm_mode = True` to seamlessly convert SQLAlchemy ORM objects to JSON
- Gift price stored as integer (likely cents)
- Optional fields allow partial gift data entry
- Clear separation between input (`Create`, `Login`) and output schemas (`Response`, `Out`)](#\schemaspy)

---

- [\__init__.py](#\initpy)
- [# Summary

**Purpose:** This is a Python package initialization file (`__init__.py`).

**Key Points:**
- Empty or minimal file that marks its parent directory as a Python package
- Allows the directory to be imported as a module in Python
- No significant logic or functions defined
- Typically used in package structure to enable `from package import module` syntax](#\initpy)

---

- [\app\main.py](#\app\mainpy)
- [# Code Summary

**Purpose:** Main entry point for a FastAPI application called "Gifters"

**Key Logic:**
- Initializes a FastAPI application instance with the title "Gifters"
- Registers a router from the `routes.gifts` module to handle gift-related endpoints

**Key Components:**
- `FastAPI()` - Creates the ASGI web application
- `app.include_router()` - Mounts the gifts router to integrate gift-related API routes

This is a minimal application setup that delegates all route handling to a separate `gifts` router module.](#\app\mainpy)

---

- [\routes\auths.py](#\routes\authspy)
- [# Summary

**Purpose**: FastAPI authentication module for Google OAuth2 integration with JWT token generation.

**Key Components**:

1. **OAuth Setup**: Configures Google OAuth2 client with credentials from environment variables, defining authorization endpoints and required scopes (openid, email, profile)

2. **Database Dependency**: `get_db()` function provides database session management with proper cleanup

3. **Commented Callback Logic**: The core functionality (currently disabled) handles:
   - Google OAuth token exchange and ID token parsing
   - User lookup/creation in `ExternalUser` table via Google ID
   - JWT token generation with user metadata (user_id, email, role)
   - Frontend redirect with bearer token

**Current State**: The Google login and callback routes are commented out, so the module is set up but not actively serving authentication requests. The infrastructure is in place for OAuth flow once uncommented.](#\routes\authspy)

---

- [\routes\gifts.py](#\routes\giftspy)
- [# Summary: FastAPI Gift Management Router

## Purpose
This file implements a REST API router for managing gifts using FastAPI. It provides endpoints to fetch, search, and add gifts with JWT token authentication.

## Key Components

**Pydantic Models:**
- `GiftCreate`: Input schema for creating gifts (name, brand, size, color)
- `GiftPatch`: Partial update schema with optional fields
- `Gift`: Complete gift model with ID

**Endpoints:**

1. **GET `/gifts/fetch/{user_id}`**
   - Fetches all gifts for a specific user
   - Requires JWT authorization header
   - Validates token before returning gifts
   - Returns `List[GiftResponse]`

2. **GET `/gifts/searchby/{column}/{value}`**
   - Searches gifts by dynamic column (id, name, brand, size, color, user_id)
   - Validates column exists in allowed list
   - Case-insensitive, whitespace-trimmed search using SQLAlchemy `func.lower()`

3. **POST `/gifts/add/{user_id}`** (incomplete)
   - Adds new gift for user
   - Requires JWT authorization header
   - Uses `GiftTemplate` input schema

**Key Logic:**
- `get_db()`: Dependency injection function managing database session lifecycle
- Dynamic column attribute fetching using `getattr()` for flexible searching
- JWT token extraction and validation from Authorization header
- Error handling with appropriate HTTP status codes (401 for auth, 404 for not found)

**Dependencies:** FastAPI, SQLAlchemy ORM, Pydantic, JWT authentication utilities](#\routes\giftspy)

---

- [\routes\share.py](#\routes\sharepy)
- [# Summary: Shareable Gift List Links API

## Purpose
FastAPI router that creates and retrieves shareable gift lists via unique tokens, allowing users to share their gift collections with others.

## Key Logic

**POST `/share/{user_id}`** - Creates a sharable link
- Generates a new `GiftsList` record for a user
- Returns a shareable URL containing an auto-generated `share_token`
- Includes SQLAlchemy error handling with rollback on failure

**GET `/share/token/{token}`** - Retrieves gifts via token
- Validates the share token against the database
- Fetches the associated gift list owner and all their gifts
- Returns owner ID and complete gift list, or 401 error if token invalid

## Important Components
- **Router prefix**: `/share` with sharable links tag
- **Dependencies**: Database session injection via `get_db`
- **Models used**: `GiftsList` (owns share_token), `Gifts` (user's gift items)
- **Error handling**: SQLAlchemy exceptions caught with HTTP 500; invalid tokens return 401](#\routes\sharepy)

---

- [\routes\users.py](#\routes\userspy)
- [# Code Summary

## Purpose
This is a FastAPI user authentication and management router that handles user registration, login, and token-based access control.

## Key Components

**Main Functions:**
1. **`get_current_user()`** - Dependency function that validates JWT tokens and returns the authenticated user from the database. Raises 401 error for invalid/expired tokens.

2. **`search_user(id)`** - GET endpoint that retrieves a user by ID from the database.

3. **`post_user()`** - POST endpoint to create a new user directly from UserCreate schema data.

4. **`register_user()`** - POST endpoint for user registration that:
   - Checks for duplicate emails
   - Hashes passwords using `hash_password()`
   - Stores user with both plain and hashed password in database

5. **`login/basic`** - Incomplete login endpoint (code cut off)

## Key Logic
- Uses OAuth2PasswordBearer for token-based authentication
- JWT tokens decoded with `jose` library for user verification
- Password hashing integrated via utils
- Database operations via SQLAlchemy ORM sessions
- Input validation using Pydantic schemas (UserCreate, UserResponse, etc.)

## Notable Issues
- Mixed authentication: stores both plain and hashed passwords (security risk)
- Incomplete login endpoint
- Unused `users_list` variable referenced
- Some dead/commented-out code present](#\routes\userspy)

---

- [\utils\auth.py](#\utils\authpy)
- [# Security/Authentication Module Summary

**Purpose:** Handles password hashing, JWT token validation, and user authentication for a FastAPI application.

## Key Components:

1. **Password Management:**
   - `hash_password()` - Hashes passwords using bcrypt_sha256 algorithm via Passlib
   - `verify_password()` - Validates plain text passwords against stored hashes

2. **JWT Authentication:**
   - `oauth2_scheme` - OAuth2 password bearer token scheme for extracting tokens from requests
   - `SECRET_KEY` & `ALGORITHM` - Configuration for JWT encoding/decoding (HS256)

3. **Main Logic - `get_user()` function:**
   - Dependency injection function that validates JWT tokens from HTTP requests
   - Decodes JWT token to extract user email from `sub` claim
   - Queries database to retrieve User object by email
   - Raises 401 HTTPException if token is invalid or user not found
   - Returns authenticated User object for use in route handlers

**Key Flow:** Token → JWT decode → Extract email → Database lookup → Return user or raise auth error](#\utils\authpy)

---

- [\utils\jwt_handlers.py](#\utils\jwthandlerspy)
- [# JWT Token Authentication Module

**Purpose:** Handles JWT token creation and verification for API authentication.

## Key Components:

1. **Constants:**
   - `SECRET_KEY`: Signing key for tokens (hardcoded - should be environment variable)
   - `ALGORITHM`: HS256 for token signing
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30-minute default token lifetime

2. **`create_acces_token()`** [Note: typo in function name]
   - Creates signed JWT tokens
   - Accepts custom data dict and optional expiration delta
   - Sets `exp` claim to current UTC time + expiration duration
   - Returns encoded JWT string

3. **`verify_token()`**
   - Decodes and validates JWT tokens
   - Returns payload dict if valid
   - Returns `None` on JWTError (invalid/expired token)

**Security Notes:** The hardcoded `SECRET_KEY` is a vulnerability—should use environment variables in production.](#\utils\jwthandlerspy)

---


---

