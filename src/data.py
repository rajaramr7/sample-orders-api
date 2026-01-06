"""In-memory test data for the sample orders API."""

from typing import Dict, Any
from copy import deepcopy

# Orders database - keyed by order_id
_ORDERS_DB: Dict[int, Dict[str, Any]] = {
    1001: {
        "order_id": 1001,
        "user_id": "user_a",
        "product_name": "Widget A",
        "price": 99.99,
        "status": "shipped",
        "created_at": "2024-01-15T10:30:00Z"
    },
    1002: {
        "order_id": 1002,
        "user_id": "user_a",
        "product_name": "Widget B",
        "price": 149.99,
        "status": "pending",
        "created_at": "2024-01-16T14:20:00Z"
    },
    1003: {
        "order_id": 1003,
        "user_id": "user_a",
        "product_name": "Widget C",
        "price": 199.99,
        "status": "delivered",
        "created_at": "2024-01-17T09:15:00Z"
    },
    2001: {
        "order_id": 2001,
        "user_id": "user_b",
        "product_name": "Gadget X",
        "price": 299.99,
        "status": "pending",
        "created_at": "2024-01-18T11:45:00Z"
    },
    2002: {
        "order_id": 2002,
        "user_id": "user_b",
        "product_name": "Gadget Y",
        "price": 399.99,
        "status": "shipped",
        "created_at": "2024-01-19T16:00:00Z"
    }
}

# User profiles database - keyed by user_id
_PROFILES_DB: Dict[str, Dict[str, Any]] = {
    "user_a": {
        "user_id": "user_a",
        "email": "user_a@example.com",
        "full_name": "Alice Anderson",
        "phone": "+1-555-0101",
        "address": "123 Main St, Anytown, USA"
    },
    "user_b": {
        "user_id": "user_b",
        "email": "user_b@example.com",
        "full_name": "Bob Brown",
        "phone": "+1-555-0102",
        "address": "456 Oak Ave, Somewhere, USA"
    },
    "admin": {
        "user_id": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "phone": "+1-555-0100",
        "address": "789 Admin Blvd, HQ, USA"
    }
}

# Counter for generating new order IDs
_next_order_id = 3001


def get_next_order_id() -> int:
    """Get the next available order ID."""
    global _next_order_id
    order_id = _next_order_id
    _next_order_id += 1
    return order_id


# Orders CRUD operations
def get_all_orders() -> list:
    """Get all orders."""
    return list(_ORDERS_DB.values())


def get_orders_by_user(user_id: str) -> list:
    """Get orders for a specific user."""
    return [order for order in _ORDERS_DB.values() if order["user_id"] == user_id]


def get_order_by_id(order_id: int) -> Dict[str, Any] | None:
    """Get a single order by ID."""
    return _ORDERS_DB.get(order_id)


def create_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new order."""
    order_id = get_next_order_id()
    order = {
        "order_id": order_id,
        **order_data
    }
    _ORDERS_DB[order_id] = order
    return order


def update_order(order_id: int, order_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update an existing order."""
    if order_id not in _ORDERS_DB:
        return None
    _ORDERS_DB[order_id].update(order_data)
    return _ORDERS_DB[order_id]


def delete_order(order_id: int) -> bool:
    """Delete an order."""
    if order_id in _ORDERS_DB:
        del _ORDERS_DB[order_id]
        return True
    return False


# Profile CRUD operations
def get_profile(user_id: str) -> Dict[str, Any] | None:
    """Get a user profile."""
    return _PROFILES_DB.get(user_id)


def update_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update a user profile."""
    if user_id not in _PROFILES_DB:
        return None
    _PROFILES_DB[user_id].update(profile_data)
    return _PROFILES_DB[user_id]
