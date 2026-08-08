from fastapi import APIRouter, Depends, HTTPException, status
from httpx import ConnectError, TimeoutException
from supabase_auth.errors import AuthApiError, AuthInvalidCredentialsError

from schemas import UserAuth
from database import supabase
from routes.dependencies import get_authenticated_user, serialize_supabase_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserAuth):

    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password
            }
        )
    except (AuthApiError, ConnectError, TimeoutException) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to complete signup") from exc

    if response.user is None:
        raise HTTPException(status_code=500, detail="Supabase did not return a user")

    return {
        "user": serialize_supabase_user(response.user)
    }

@router.post("/login")
def login(user: UserAuth):

    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password
            }
        )

        if response.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials"
            )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except (AuthInvalidCredentialsError, AuthApiError):

        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )
    except (ConnectError, TimeoutException) as exc:
        raise HTTPException(
            status_code=503,
            detail="Supabase auth service unavailable"
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to complete login"
        ) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(auth = Depends(get_authenticated_user)):
    try:
        supabase.auth.admin.sign_out(auth["token"])
    except (ConnectError, TimeoutException) as exc:
        raise HTTPException(status_code=503, detail="Supabase auth service unavailable") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return None