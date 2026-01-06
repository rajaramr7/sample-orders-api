"""Orders routes."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import get_current_user
from ..models import OrderCreate, OrderUpdate, OrderResponse
from .. import data

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=List[OrderResponse])
async def list_orders(current_user: dict = Depends(get_current_user)):
    """
    List orders.

    - Regular users see only their own orders.
    - Admins see all orders.
    """
    if current_user["role"] == "admin":
        orders = data.get_all_orders()
    else:
        orders = data.get_orders_by_user(current_user["user_id"])

    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, current_user: dict = Depends(get_current_user)):
    """
    Get a single order by ID.

    - Regular users can only access their own orders.
    - Admins can access any order.
    """
    order = data.get_order_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check authorization
    if current_user["role"] != "admin" and order["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )

    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new order.

    The order will be associated with the authenticated user.
    """
    new_order = data.create_order({
        "user_id": current_user["user_id"],
        "product_name": order_data.product_name,
        "price": order_data.price,
        "status": order_data.status,
        "created_at": datetime.utcnow().isoformat() + "Z"
    })

    return new_order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing order.

    - Regular users can only update their own orders.
    - Admins can update any order.
    """
    order = data.get_order_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check authorization
    if current_user["role"] != "admin" and order["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order"
        )

    # Build update dict with only provided fields
    update_dict = {}
    if order_data.product_name is not None:
        update_dict["product_name"] = order_data.product_name
    if order_data.price is not None:
        update_dict["price"] = order_data.price
    if order_data.status is not None:
        update_dict["status"] = order_data.status

    updated_order = data.update_order(order_id, update_dict)
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, current_user: dict = Depends(get_current_user)):
    """
    Delete an order.

    - Regular users can only delete their own orders.
    - Admins can delete any order.
    """
    order = data.get_order_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check authorization
    if current_user["role"] != "admin" and order["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this order"
        )

    data.delete_order(order_id)
    return None
