# Sample Orders API

A sample FastAPI application for testing the APIsec agent.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
./run.sh
```

The API will be available at `http://localhost:8000`.

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Authentication

The API uses JWT-based authentication. Get a token using one of these methods:

### Password Grant (for users)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "password", "username": "user_a", "password": "password_a"}'
```

### Client Credentials Grant (for service accounts)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "client_credentials", "client_id": "service_account", "client_secret": "service_secret"}'
```

## Test Users

| Username | Password | Role | Owned Orders |
|----------|----------|------|--------------|
| user_a | password_a | user | 1001, 1002, 1003 |
| user_b | password_b | user | 2001, 2002 |
| admin | admin_password | admin | (all) |

## Service Account

| Client ID | Client Secret | Role |
|-----------|---------------|------|
| service_account | service_secret | admin |

## Endpoints

### Authentication
- `POST /auth/token` - Get access token

### Orders
- `GET /orders` - List orders (filtered by user, admin sees all)
- `GET /orders/{id}` - Get single order
- `POST /orders` - Create order
- `PUT /orders/{id}` - Update order
- `DELETE /orders/{id}` - Delete order

### Users
- `GET /users/{id}/profile` - Get user profile
- `PUT /users/{id}/profile` - Update user profile

## Example Usage

```bash
# Get a token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "password", "username": "user_a", "password": "password_a"}' \
  | jq -r '.access_token')

# List orders
curl -X GET http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN"

# Create an order
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "New Widget", "price": 59.99}'
```

## Test Data

The API comes with pre-loaded test orders:

| Order ID | User | Product | Price | Status |
|----------|------|---------|-------|--------|
| 1001 | user_a | Widget A | $99.99 | shipped |
| 1002 | user_a | Widget B | $149.99 | pending |
| 1003 | user_a | Widget C | $199.99 | delivered |
| 2001 | user_b | Gadget X | $299.99 | pending |
| 2002 | user_b | Gadget Y | $399.99 | shipped |
