from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import supabase

bearer_scheme = HTTPBearer(auto_error=False)


def serialize_supabase_user(user):
    return {
        "id": getattr(user, "id", None),
        "email": getattr(user, "email", None),
        "created_at": getattr(user, "created_at", None),
    }


def get_authenticated_user(credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme)):
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        ) from exc

    user = getattr(response, "user", None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {
        "token": token,
        "user": user,
    }