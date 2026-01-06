# Sample Orders API

A sample FastAPI application for testing the APIsec agent. This API simulates a basic e-commerce orders system with JWT authentication and role-based access control.

## Table of Contents

- [Installation](#installation)
- [Running Locally](#running-locally)
- [Environment Configuration](#environment-configuration)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Test Users & Permissions](#test-users--permissions)
- [API Endpoints](#api-endpoints)
- [Sample curl Commands](#sample-curl-commands)
- [Test Data](#test-data)
- [Project Structure](#project-structure)

## Installation

### Prerequisites

- Python 3.9+
- pip

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/rajaramr7/sample-orders-api.git
cd sample-orders-api

# Option 1: Using the run script (creates venv automatically)
./run.sh

# Option 2: Manual installation
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Locally

### Using the run script (recommended)

```bash
./run.sh
```

This will:
1. Create a virtual environment if it doesn't exist
2. Install dependencies
3. Start the server on http://localhost:8000

### Manual start

```bash
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Verify the server is running

```bash
curl http://localhost:8000/health
# Response: {"status":"healthy"}
```

## Environment Configuration

Environment files are located in the `config/` directory:

| File | Purpose |
|------|---------|
| `config/dev.env` | Local development settings |
| `config/staging.env` | Staging environment settings |

### Development Environment

```bash
# config/dev.env
BASE_URL=http://localhost:8000
AUTH_ENDPOINT=http://localhost:8000/auth/token
LOG_LEVEL=DEBUG
```

### Staging Environment

```bash
# config/staging.env
BASE_URL=https://staging-api.orders.example.com
AUTH_ENDPOINT=https://staging-api.orders.example.com/auth/token
LOG_LEVEL=INFO
```

## API Documentation

When running locally, interactive API documentation is available at:

| Documentation | URL |
|---------------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |
| OpenAPI YAML | [docs/openapi.yaml](docs/openapi.yaml) |

## Authentication

The API uses JWT Bearer token authentication. Tokens expire after 30 minutes.

### Getting a Token

#### Password Grant (for end users)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "password",
    "username": "user_a",
    "password": "password_a"
  }'
```

#### Client Credentials Grant (for service accounts)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "service_account",
    "client_secret": "service_secret"
  }'
```

#### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using the Token

Include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/orders
```

### Token Payload

The JWT token contains:
- `sub`: User ID (e.g., "user_a", "admin")
- `role`: User role ("user" or "admin")
- `exp`: Expiration timestamp

## Test Users & Permissions

### User Accounts (Password Grant)

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| `user_a` | `password_a` | user | Can access own orders (1001, 1002, 1003) and own profile |
| `user_b` | `password_b` | user | Can access own orders (2001, 2002) and own profile |
| `admin` | `admin_password` | admin | Can access ALL orders and ALL profiles |

### Service Account (Client Credentials Grant)

| Client ID | Client Secret | Role | Permissions |
|-----------|---------------|------|-------------|
| `service_account` | `service_secret` | admin | Full access to all resources |

### Permission Matrix

| Action | Regular User | Admin |
|--------|--------------|-------|
| List own orders | ✅ | ✅ |
| List all orders | ❌ | ✅ |
| View own order | ✅ | ✅ |
| View any order | ❌ | ✅ |
| Create order | ✅ (owns it) | ✅ |
| Update own order | ✅ | ✅ |
| Update any order | ❌ | ✅ |
| Delete own order | ✅ | ✅ |
| Delete any order | ❌ | ✅ |
| View own profile | ✅ | ✅ |
| View any profile | ❌ | ✅ |
| Update own profile | ✅ | ✅ |
| Update any profile | ❌ | ✅ |

## API Endpoints

### Health Check

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | No | Service status |
| GET | `/health` | No | Health check |

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/token` | No | Get access token |

### Orders

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/orders` | Yes | List orders |
| GET | `/orders/{id}` | Yes | Get single order |
| POST | `/orders` | Yes | Create new order |
| PUT | `/orders/{id}` | Yes | Update order |
| DELETE | `/orders/{id}` | Yes | Delete order |

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/users/{id}/profile` | Yes | Get user profile |
| PUT | `/users/{id}/profile` | Yes | Update user profile |

## Sample curl Commands

### Setup: Get a token and store it

```bash
# Get token for user_a
export TOKEN=$(curl -s -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "password", "username": "user_a", "password": "password_a"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Health Check

```bash
# Check service status
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health
```

### Orders - List

```bash
# List orders (user sees own orders, admin sees all)
curl -X GET http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN"
```

### Orders - Get Single

```bash
# Get order by ID
curl -X GET http://localhost:8000/orders/1001 \
  -H "Authorization: Bearer $TOKEN"
```

### Orders - Create

```bash
# Create a new order
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wireless Keyboard",
    "price": 79.99,
    "status": "pending"
  }'
```

### Orders - Update

```bash
# Update order status
curl -X PUT http://localhost:8000/orders/1001 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped"
  }'

# Update multiple fields
curl -X PUT http://localhost:8000/orders/1001 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Updated Widget",
    "price": 109.99,
    "status": "delivered"
  }'
```

### Orders - Delete

```bash
# Delete an order
curl -X DELETE http://localhost:8000/orders/1001 \
  -H "Authorization: Bearer $TOKEN"
```

### Profile - Get

```bash
# Get own profile
curl -X GET http://localhost:8000/users/user_a/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Profile - Update

```bash
# Update profile
curl -X PUT http://localhost:8000/users/user_a/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "phone": "+1-555-9999"
  }'
```

### Testing Authorization (403 Forbidden)

```bash
# As user_a, try to access user_b's order (should return 403)
curl -X GET http://localhost:8000/orders/2001 \
  -H "Authorization: Bearer $TOKEN"

# As user_a, try to access user_b's profile (should return 403)
curl -X GET http://localhost:8000/users/user_b/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Testing with Admin Token

```bash
# Get admin token
export ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "password", "username": "admin", "password": "admin_password"}' \
  | jq -r '.access_token')

# Admin can access any order
curl -X GET http://localhost:8000/orders/2001 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Admin can access any profile
curl -X GET http://localhost:8000/users/user_b/profile \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Test Data

### Pre-loaded Orders

| Order ID | User | Product | Price | Status |
|----------|------|---------|-------|--------|
| 1001 | user_a | Widget A | $99.99 | shipped |
| 1002 | user_a | Widget B | $149.99 | pending |
| 1003 | user_a | Widget C | $199.99 | delivered |
| 2001 | user_b | Gadget X | $299.99 | pending |
| 2002 | user_b | Gadget Y | $399.99 | shipped |

### Pre-loaded User Profiles

| User ID | Email | Full Name |
|---------|-------|-----------|
| user_a | user_a@example.com | Alice Anderson |
| user_b | user_b@example.com | Bob Brown |
| admin | admin@example.com | Admin User |

## Project Structure

```
sample-orders-api/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── auth.py          # JWT authentication logic
│   ├── data.py          # In-memory data store
│   ├── models.py        # Pydantic models
│   └── routes/
│       ├── __init__.py
│       ├── auth.py      # /auth/token endpoint
│       ├── orders.py    # /orders endpoints
│       └── users.py     # /users endpoints
├── config/
│   ├── dev.env          # Development environment
│   └── staging.env      # Staging environment
├── docs/
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── logs/
│   └── staging-access.log  # Sample access logs
├── postman/
│   ├── orders-api.postman_collection.json
│   └── orders-api.postman_environment.json
├── requirements.txt
├── run.sh
└── README.md
```

## Additional Resources

- **Postman Collection**: Import `postman/orders-api.postman_collection.json` for ready-to-use API requests
- **OpenAPI Spec**: Use `docs/openapi.yaml` for API documentation or code generation
- **Sample Logs**: `logs/staging-access.log` contains example API access logs
