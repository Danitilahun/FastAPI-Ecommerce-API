from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.schemas.products import ProductBase, CategoryBase


# Base Config
class BaseConfig:
    from_attributes = True


class ProductBaseOrder(ProductBase):
    category: CategoryBase = Field(exclude=True)

    class Config(BaseConfig):
        pass


# Base Order & Order_Item (Changed Class Names)
class OrderItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: ProductBaseOrder  # Changed type

class OrderBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    order_items: List[OrderItemBase]  # Changed attribute name

    class Config(BaseConfig):
        pass


class OrderOutBase(BaseModel): #Changed class name
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    order_items: List[OrderItemBase]  # Changed attribute name

    class Config(BaseConfig):
        pass


# Get Order (Changed Class Name)
class OrderOut(BaseModel):
    message: str
    data: OrderBase

    class Config(BaseConfig):
        pass


class OrdersOutList(BaseModel):  # Changed class name
    message: str
    data: List[OrderBase]

class OrdersUserOutList(BaseModel):
    message: str
    data: List[OrderBase]

    class Config(BaseConfig):
        pass

# Delete Order(Changed Class Name)
class OrderOutDelete(BaseModel):
    message: str
    data: OrderOutBase


# Create Order (Changed Class Name)
class OrderItemCreate(BaseModel):  # Changed Class Name
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate] #Changed Class Name

    class Config(BaseConfig):
        pass


# Update Order (Changed Class Name)
class OrderUpdate(OrderCreate):
    pass