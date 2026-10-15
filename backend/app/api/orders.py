from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Order, OrderItem, OrderStatus
from app.db.session import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderItemOut(BaseModel):
    product_name: str
    sku: str
    quantity: int
    unit_price: Decimal


class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    status: OrderStatus
    total_amount: Decimal
    ordered_at: datetime
    delivered_at: datetime | None
    tracking_number: str | None
    items: list[OrderItemOut]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderOut:
    order = db.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
        )
    )
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    return OrderOut(
        id=order.id,
        customer_name=order.customer.name,
        customer_email=order.customer.email,
        status=order.status,
        total_amount=order.total_amount,
        ordered_at=order.ordered_at,
        delivered_at=order.delivered_at,
        tracking_number=order.tracking_number,
        items=[
            OrderItemOut(
                product_name=item.product.name,
                sku=item.product.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in order.items
        ],
    )