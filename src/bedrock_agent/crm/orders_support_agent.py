import os

import boto3

from bedrock_agent.crm.non_collaborating_agent import NonCollaboratingAgent
from bedrock_agent.utils.inline_agent_utils import load_json_file
from bedrock_agent.utils.lambda_creator import create_lambda_function_and_its_resources, \
    remove_lambda_function_and_its_resources

ORDER_SUPPORT_AGENT_LAMBDA_NAME = "inline-agent-order-handler"
ORDER_SUPPORT_AGENT_BUCKET_NAME = "inline-agent-sample-orders-bucket"


class OrderSupportAgent(NonCollaboratingAgent):
    def __init__(self, aws_region: str,foundational_model: str = None, session_id: str = None):
        instructions = (
            "You are the Order Support Agent. Your primary goal is to provide detailed, accurate, and helpful information "
            "about the orders. Use only the information from the provided tools. If order is not available, "
            "do not make up information, tell that you do not know."
            "\nNext to fetching information, you also have the ability to create, update and delete orders. "
        )
        super().__init__(instructions, foundational_model, session_id)
        self.name = "Order Support Agent"
        self.lambda_name = ORDER_SUPPORT_AGENT_LAMBDA_NAME
        self.bucket_name = ORDER_SUPPORT_AGENT_BUCKET_NAME

        sts_client = boto3.client("sts")
        self.account_id = sts_client.get_caller_identity()["Account"]
        self.aws_region = aws_region

        # Initialise the ActionGroup
        self._verify_lambda()
        self._add_action_group()

    def _verify_lambda(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(__file__)

        # Construct the path to lambda_function_order_handler.py
        lambda_function_path = os.path.join(script_dir, "lambdas","lambda_function_order_handler.py")

        resources = create_lambda_function_and_its_resources(
            region=self.aws_region,
            account_id=self.account_id,
            custom_name=self.lambda_name,
            lambda_code_path=lambda_function_path,
            bucket_name=self.bucket_name,
        )
        lambda_function = resources['lambda_function']
        self.lambda_function_arn = lambda_function['FunctionArn']

    def _add_action_group(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(__file__)

        # Construct the path to lambda_function_order_handler.py
        handle_orders_file = os.path.join(script_dir, "lambdas","payload-orders.json")
        handle_orders_payload = load_json_file(handle_orders_file)

        self.action_group = {
            "name": "HandleOrders",
            "executor": self.lambda_function_arn,
            "payload": handle_orders_payload,
            "description": "This action group handles the orders."
        }

    def clean_up(self):
        """Clean up the resources used by the agent"""
        # Remove the lambda function and its resources
        remove_lambda_function_and_its_resources(
            region=self.aws_region,
            account_id=self.account_id,
            custom_name=self.lambda_name,
            bucket_name=self.bucket_name,
        )
