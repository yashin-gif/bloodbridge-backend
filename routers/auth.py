from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.auth import Token, ForgotPasswordRequest, ResetPasswordRequest
from schemas.user import UserCreate, UserLogin, UserResponse
from utils.security import ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token,hash_password,verify_password,create_password_reset_token,decode_password_reset_token

router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate,db: Session = Depends(get_db)):

    existing_username = db.query(User).filter(User.username == user_data.username).first()

    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")

    existing_email = db.query(User).filter(User.email == user_data.email).first()

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")

    existing_phone = db.query(User).filter(User.phone == user_data.phone).first()

    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        blood_group=user_data.blood_group,
        location=user_data.location
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(user_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")

    if not verify_password(user_data.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Account is inactive")

    access_token = create_access_token(data={"user_id": user.id,"username": user.username,"role": user.role},expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token,"token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(user_data: ForgotPasswordRequest,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email does not exist")

    reset_token = create_password_reset_token(user.id)

    return {"message": "Password reset token generated successfully","reset_token": reset_token}


@router.post("/reset-password")
def reset_password(user_data: ResetPasswordRequest,db: Session = Depends(get_db)):

    payload = decode_password_reset_token(user_data.token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired reset token")

    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    user.password_hash = hash_password(user_data.new_password)

    db.commit()

    return {"message": "Password reset successfully"}