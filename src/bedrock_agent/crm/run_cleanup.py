import boto3

from bedrock_agent.crm.orders_support_agent import ORDER_SUPPORT_AGENT_LAMBDA_NAME, ORDER_SUPPORT_AGENT_BUCKET_NAME
from bedrock_agent.utils.lambda_creator import remove_lambda_function_and_its_resources

if __name__ == "__main__":
    sts_client = boto3.client("sts")

    # Example usage
    region = "eu-west-1"
    account_id = sts_client.get_caller_identity()["Account"]

    # Remove Lambda function for Order Support Agent
    remove_lambda_function_and_its_resources(
        region,
        account_id,
        ORDER_SUPPORT_AGENT_LAMBDA_NAME,
        ORDER_SUPPORT_AGENT_BUCKET_NAME
    )