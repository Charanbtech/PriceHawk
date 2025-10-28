# backend/core/schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr, HttpUrl, validator
from typing import Optional, List, Dict, Union, Any

# -------------------------------
# USER SCHEMAS
# -------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=64)
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    created_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=64)] = None


# -------------------------------
# PRODUCT SCHEMAS
# -------------------------------
class ProductSearchIn(BaseModel):
    query: str
    sources: Optional[List[str]] = Field(default_factory=list)
    max_results: int = 10
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class ProductOut(BaseModel):
    title: str
    price: float
    currency: str = "USD"
    url: str
    source: str
    product_id: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    in_stock: Optional[bool] = True
    category: Optional[str] = None


# -------------------------------
# TRACKING SCHEMAS
# -------------------------------
class TrackProductRequest(BaseModel):
    name: str
    url: str
    current_price: float
    original_price: Optional[float] = None
    currency: str = "USD"
    source: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    in_stock: bool = True
    target_price: Optional[float] = None
    notify_on_price_drop: bool = True
    notify_on_availability: bool = True

    @validator('target_price')
    def target_price_must_be_less_than_current(cls, v, values):
        if v is not None and 'current_price' in values:
            current = values.get('current_price', 0)
            if current > 0 and v >= current:
                raise ValueError('Target price must be less than current price')
        return v

class UpdateTrackingRequest(BaseModel):
    target_price: Optional[float] = None
    notify_on_price_drop: Optional[bool] = None
    notify_on_availability: Optional[bool] = None

    class Config:
        extra = "forbid"


# -------------------------------
# PRICE HISTORY SCHEMAS
# -------------------------------
class PricePoint(BaseModel):
    price: float
    date: datetime


# -------------------------------
# NOTIFICATION SCHEMAS
# -------------------------------
class NotificationRequest(BaseModel):
    user_id: str
    type: str  # price_drop, back_in_stock, test, etc.
    message: str
    product_id: Optional[str] = None
    old_price: Optional[float] = None
    new_price: Optional[float] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    product_name: Optional[str] = None

class NotificationPreferences(BaseModel):
    email_notifications: bool = True
    push_notifications: bool = False
    notification_frequency: str = "immediate"  # immediate, daily, weekly
    email: Optional[EmailStr] = None


# -------------------------------
# FORECAST SCHEMAS
# -------------------------------
class ForecastPoint(BaseModel):
    date: str
    price: float
    price_lower: Optional[float] = None
    price_upper: Optional[float] = None
    is_prediction: bool = True

class PriceForecast(BaseModel):
    product_id: str
    forecast: List[ForecastPoint]
    trend: str  # increasing, decreasing, stable, unknown
    best_buy: Dict[str, Any]  # date and price
