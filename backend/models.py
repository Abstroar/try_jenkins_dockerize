from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str
    name: str
    profile_image: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Portfolio(BaseModel):
    id: Optional[str] = None
    user_id: str
    symbols: List[str] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    profile_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PortfolioResponse(BaseModel):
    id: str
    user_id: str
    symbols: List[str]
    created_at: datetime
    updated_at: datetime 