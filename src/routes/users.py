"""User profile routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import get_current_user
from ..models import ProfileUpdate, ProfileResponse
from .. import data

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/profile", response_model=ProfileResponse)
async def get_profile(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get a user's profile.

    - Regular users can only access their own profile.
    - Admins can access any profile.
    """
    # Check authorization
    if current_user["role"] != "admin" and user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this profile"
        )

    profile = data.get_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


@router.put("/{user_id}/profile", response_model=ProfileResponse)
async def update_profile(
    user_id: str,
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a user's profile.

    - Regular users can only update their own profile.
    - Admins can update any profile.
    """
    # Check authorization
    if current_user["role"] != "admin" and user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )

    profile = data.get_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    # Build update dict with only provided fields
    update_dict = {}
    if profile_data.email is not None:
        update_dict["email"] = profile_data.email
    if profile_data.full_name is not None:
        update_dict["full_name"] = profile_data.full_name
    if profile_data.phone is not None:
        update_dict["phone"] = profile_data.phone
    if profile_data.address is not None:
        update_dict["address"] = profile_data.address

    updated_profile = data.update_profile(user_id, update_dict)
    return updated_profile
