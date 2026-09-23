from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import BloodRequest, Donation, User
from schemas.user import UserResponse
from utils.permissions import require_admin

router = APIRouter(prefix="/admin",tags=["Admin"])

@router.get("/users",response_model=list[UserResponse])
def get_all_users(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    require_admin(current_user)
    return db.query(User).all()

@router.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    
    require_admin(current_user)
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.put("/users/{user_id}/status",response_model=UserResponse)
def change_user_status(user_id: int,is_active: bool,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    require_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return user

@router.put("/users/{user_id}/role",response_model=UserResponse)
def change_user_role(user_id: int,role: str,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    require_admin(current_user)

    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400,detail="Role must be user or admin")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    user.role = role

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    require_admin(current_user)

    if user_id == current_user.id:

        raise HTTPException(status_code=400,detail="Admin cannot delete their own account")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.get("/blood-requests")
def get_all_blood_requests(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    require_admin(current_user)
    return db.query(BloodRequest).all()


@router.get("/donations")
def get_all_donations(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    require_admin(current_user)
    
    return db.query(Donation).all()