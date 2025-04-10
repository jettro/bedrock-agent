import os
import pickle

from dotenv import load_dotenv
from pandas import DataFrame

from bedrock_agent.crm.models import UserInfo, Order

_ = load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
database_file_path = os.path.join(base_dir, "../../../export/database.pickl")


def load_orders() -> DataFrame:
    """Load the orders from the database"""
    with open(database_file_path, 'rb') as f:
        data = pickle.load(f)

    return data


def init_database():
    """Initialize the database with some orders"""
    data = DataFrame({
        "user_id": ["1", "2"],
        "order_id": ["123", "124"],
        "status": ["shipped", "processing"],
        "delivery_date": ["2022-06-15", None]
    })

    with open(database_file_path, 'wb') as file_write:
        pickle.dump(data, file_write)


def find_order_information_for_user(user_info: UserInfo, order_id: str) -> Order | None:
    """Find the information about an order, if no order is found return a message
    telling that the order was not found.

    Args:
        user_info(UserInfo): The user information to find the order for
        order_id (str): The order id to find the information for
    """
    orders = load_orders()
    user_orders = orders.query("user_id == @user_info.user_id and order_id == @order_id")

    if user_orders.empty:
        return None

    order = user_orders.iloc[0]
    return Order(
        user_id=order["user_id"],
        order_id=order["order_id"],
        status=order["status"],
        delivery_date=order["delivery_date"]
    )


def main():
    # Check for existing database
    if not os.path.exists(database_file_path):
        init_database()


if __name__ == "__main__":
    main()