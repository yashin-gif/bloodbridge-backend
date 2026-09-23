from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String, Text)
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    blood_group = Column(String(5), nullable=True)
    location = Column(String(100), nullable=True)
    role = Column(String(20), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_available = Column(Boolean, default=False, nullable=False)
    created_at = Column( DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    blood_group = Column(String(5), nullable=False)
    units_required = Column(Integer, default=1, nullable=False)
    hospital_name = Column(String(150), nullable=False)
    location = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    urgency = Column( String(20), default="normal", nullable=False)
    required_date = Column(DateTime, nullable=True)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False)

    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)



class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blood_request_id = Column(Integer, ForeignKey("blood_requests.id"), nullable=False)
    donation_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)