from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    """Schema para criação de lead"""
    name: str
    email: EmailStr
    phone: str


class LeadResponse(BaseModel):
    """Schema de resposta do lead"""
    id: str
    name: str
    email: str
    phone: str
    birth_date: Optional[str] = None


class LeadInDB(BaseModel):
    """Schema do lead no banco"""
    name: str
    email: str
    phone: str
    birth_date: Optional[str]
    created_at: datetime
