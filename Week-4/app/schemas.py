from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: str | None = None
    password: str | None = None