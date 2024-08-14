from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request

from src.auth.dependencies import get_current_active_auth_user
from src.order.service import OrderService
from src.order.schemas import OrderCreate, OrderRead
from src.users.schemas import UserRead


router = APIRouter(prefix='/order', tags=['Order'])


@router.get('/', response_model=list[OrderRead])
async def get_orders(service: Annotated[OrderService, Depends()]):
    orders = await service.get_orders()
    return orders


@router.post('/create')
async def create_orders(
    service: Annotated[OrderService, Depends()],
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    datasets_ids: list[int]
):
    order = OrderCreate(total_price=2)
    await service.create_order(order=order, user_id=user.id, datasets_ids=datasets_ids)
