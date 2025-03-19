from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.orders import OrderService  # Changed import
from sqlalchemy.orm import Session
from app.schemas.orders import OrderCreate, OrderUpdate, OrderOut, OrderOutDelete, OrdersOutList  # Changed import
from app.core.security import get_current_user
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(tags=["Orders"], prefix="/orders")  # Changed tag and prefix
auth_scheme = HTTPBearer()


# Get All Orders (Changed naming to match)
@router.get("/", status_code=status.HTTP_200_OK, response_model=OrdersOutList)  # Changed response model
def get_all_orders(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    return OrderService.get_all_orders(token, db, page, limit)  # Changed function call


# Get Order By User ID (Changed naming to match)
@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut)  # Changed response model
def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return OrderService.get_order(token, db, order_id)  # Changed function call


# Create New Order (Changed naming to match)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderOut)  # Changed response model
def create_order(
        order: OrderCreate, db: Session = Depends(get_db),  # Changed parameter name
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return OrderService.create_order(token, db, order)  # Changed function call


# Update Existing Order (Changed naming to match)
@router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut)  # Changed response model
def update_order(
        order_id: int,
        updated_order: OrderUpdate,  # Changed parameter name
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return OrderService.update_order(token, db, order_id, updated_order)  # Changed function call


# Delete Order By User ID (Changed naming to match)
@router.delete("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOutDelete)  # Changed response model
def delete_order(
        order_id: int, db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return OrderService.delete_order(token, db, order_id)  # Changed function call