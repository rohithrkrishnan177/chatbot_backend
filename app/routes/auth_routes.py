from fastapi import APIRouter, HTTPException, Header
from app.schemas import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.database import users_db, token_blacklist
from app.models.user_model import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


from fastapi import HTTPException
from fastapi.responses import JSONResponse

@router.post("/signup", response_model=dict)
def signup(user_data: SignupRequest):
    if user_data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    if len(user_data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long (max 72 characters allowed)"
        )

    hashed_pw = hash_password(user_data.password)
    users_db[user_data.email] = User(email=user_data.email, hashed_password=hashed_pw)
    token = create_access_token({"sub": user_data.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Signup successful! Welcome to our service."
    }



@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest):
    user = users_db.get(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": login_data.email})
    return {"access_token": token}


@router.post("/logout")
def logout(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    token_blacklist.add(token)
    return {"message": "Logged out successfully"}


def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token invalidated")
    email = decode_access_token(token)
    if not email or email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid token or user")
    return users_db[email]
