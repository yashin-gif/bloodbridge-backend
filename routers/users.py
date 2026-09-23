from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User
from schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me",response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):

    return current_user

@router.put("/me",response_model=UserResponse)
def update_my_profile(user_data: UserUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    if user_data.phone is not None:
        existing_phone = db.query(User).filter(User.phone == user_data.phone,User.id != current_user.id).first()
        if existing_phone:
            raise HTTPException(status_code=400,detail="Phone number already exists")

    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():\
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/available-donors",response_model=list[UserResponse])
def get_available_donors(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    donors = db.query(User).filter(User.role == "user",User.is_active == True,User.is_available == True).all()
    return donors

@router.get("/donors",response_model=list[UserResponse])
def get_donors(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    donors = db.query(User).filter(User.role == "user",User.is_active == True).all()

    return donors