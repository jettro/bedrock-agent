import uuid
from abc import ABC

from bedrock_agent.crm.marketing_agent import MarketingAgent
from bedrock_agent.crm.orders_support_agent import OrderSupportAgent

DEFAULT_FOUNDATIONAL_MODEL = "eu.amazon.nova-lite-v1:0"


class FrontDeskAgent(ABC):

    def __init__(self, foundational_model: str = None, session_id: str = None, order_support_agent: OrderSupportAgent = None, marketing_agent: MarketingAgent = None):
        self.foundational_model = foundational_model if foundational_model else DEFAULT_FOUNDATIONAL_MODEL
        self.session_id = session_id if session_id else str(uuid.uuid4())
        self.order_support_agent: OrderSupportAgent = order_support_agent
        self.marketing_agent: MarketingAgent = marketing_agent

    def agent_request_params(self) -> dict:
        basic_config = {
            "enableTrace": True,
            "endSession": False,
            "foundationModel": self.foundational_model,
            "instruction": (
                "You are the Front Desk Agent. Your primary goal is to provide detailed, accurate, and helpful information "
                "about our company and orders. Your responsibility is to talk to the user to understand their needs and "
                "then relay the information to the Order Support Agent and Marketing Agent. "
            ),
            "agentCollaboration": "SUPERVISOR",
            "sessionId": self.session_id,
            "collaboratorConfigurations": [
                {
                    "collaboratorInstruction": "Use to answer questions about the company.",
                    "collaboratorName": "Marketing Agent",
                    "relayConversationHistory": "ENABLED"  # TODO: check what we need here
                },
                {
                    "collaboratorInstruction": "Use to answer questions about the company.",
                    "collaboratorName": "Order Support Agent",
                    "relayConversationHistory": "ENABLED"  # TODO: check what we need here
                },
            ],
            "collaborators": [
                self.order_support_agent.agent_request_params(),
                self.marketing_agent.agent_request_params()
            ],
        }
        return basic_config

    def prepare_input(self, input_text: str) -> dict:
        params = self.agent_request_params()
        params["inputText"] = input_text

        return params
