from fastapi import APIRouter, Depends, status

from routes.dependencies import get_authenticated_user, serialize_supabase_user

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile", status_code=status.HTTP_200_OK)
def protected_profile(auth = Depends(get_authenticated_user)):
    return serialize_supabase_user(auth["user"])


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def protected_dashboard(auth = Depends(get_authenticated_user)):
    user = auth["user"]
    return {
        "message": f"Welcome back, {getattr(user, 'email', 'user')}!",
        "user": serialize_supabase_user(user)
    }