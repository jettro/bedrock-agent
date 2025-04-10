import os
import pickle

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from pandas import DataFrame

from bedrock_agent.crm.models import UserInfo, Order

_ = load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
database_file_path = os.path.join(base_dir, "../../../export/database.pickl")

mcp = FastMCP(name="orders", settings={"user_info":UserInfo(user_id="1", user_name="Jettro")})


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

@mcp.tool()
async def find_order_information(order_id: str, ctx: Context) -> Order | str:
    """Find the information about an order, if no order is found return a message
    telling that the order was not found.

    Args:
        order_id (str): The order id to find the information for
    """
    user_info = UserInfo(user_id=os.getenv("USER_ID"), user_name=os.getenv("USER_NAME"))
    await ctx.log(level="info", message=f"Finding information about order {order_id} for user {user_info.user_name}.")
    found_order = find_order_information_for_user(user_info=user_info, order_id=order_id)

    if found_order is None:
        return f"Order with id {order_id} not found for user {user_info.user_name}."

    return found_order

def main():
    # Check for existing database
    if not os.path.exists(database_file_path):
        init_database()

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()