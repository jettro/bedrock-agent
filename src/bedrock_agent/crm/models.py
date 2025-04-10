from pydantic import BaseModel


class Order(BaseModel):
    user_id: str
    order_id: str
    status: str
    delivery_date: str


class UserInfo(BaseModel):
    user_id: str
    user_name: str
