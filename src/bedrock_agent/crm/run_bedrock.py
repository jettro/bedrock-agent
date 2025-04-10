import uuid

import boto3


from bedrock_agent.inline_agent_utils import invoke_inline_agent_helper

async def main():

    orders_action_group = {
        "name": "OrdersActionGroup",
    }

    region = "eu-west-1"

    # Runtime Endpoints
    bedrock_rt_client = boto3.client(
        "bedrock-agent-runtime",
        region_name=region
    )

    session_id = str(uuid.uuid4())
    model_id = "eu.amazon.nova-lite-v1:0"
    instruction = (
        "You are a assistant assisting in finding information about orders from users."
    )

    request_params = {
        "enableTrace": True,
        "endSession": False,
        "foundationModel": model_id,
        "instruction": instruction,
        "sessionId": session_id,
        "inputText": "Show me information about my order with id 123",
        "actionGroups": [orders_action_group]
    }

    invoke_inline_agent_helper(bedrock_rt_client, request_params, trace_level="core")