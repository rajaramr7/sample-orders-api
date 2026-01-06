"""Pydantic models for request/response validation."""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# Auth models
class TokenRequest(BaseModel):
    """Token request for OAuth2 password or client_credentials grant."""
    grant_type: Literal["password", "client_credentials"]
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


# Order models
class OrderCreate(BaseModel):
    """Request model for creating an order."""
    product_name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    status: Literal["pending", "shipped", "delivered"] = "pending"


class OrderUpdate(BaseModel):
    """Request model for updating an order."""
    product_name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["pending", "shipped", "delivered"]] = None


class OrderResponse(BaseModel):
    """Response model for an order."""
    order_id: int
    user_id: str
    product_name: str
    price: float
    status: str
    created_at: str


# Profile models
class ProfileUpdate(BaseModel):
    """Request model for updating a user profile."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ProfileResponse(BaseModel):
    """Response model for a user profile."""
    user_id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None


# Error models
class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
