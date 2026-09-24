from database import SessionLocal
from models import User


db = SessionLocal()

user = db.query(User).filter(User.id == 1).first()

if user:
    user.role = "admin"
    db.commit()
    print("User 1 is now admin.")
else:
    print("User not found.")

db.close()