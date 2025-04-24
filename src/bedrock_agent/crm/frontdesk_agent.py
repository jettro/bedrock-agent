import uuid
from abc import ABC

from bedrock_agent.crm.marketing_agent import MarketingAgent
from bedrock_agent.crm.orders_support_agent import OrderSupportAgent
from bedrock_agent.crm.product_support_agent import ProductSupportAgent

DEFAULT_FOUNDATIONAL_MODEL = "eu.amazon.nova-lite-v1:0"


class FrontDeskAgent(ABC):

    def __init__(self, foundational_model: str = None, session_id: str = None, order_support_agent: OrderSupportAgent = None, marketing_agent: MarketingAgent = None, product_support_agent: ProductSupportAgent = None):
        self.foundational_model = foundational_model if foundational_model else DEFAULT_FOUNDATIONAL_MODEL
        self.session_id = session_id if session_id else str(uuid.uuid4())
        self.order_support_agent: OrderSupportAgent = order_support_agent
        self.marketing_agent: MarketingAgent = marketing_agent
        self.product_support_agent: ProductSupportAgent = product_support_agent


    def agent_request_params(self) -> dict:
        basic_config = {
            # "agentName": "front_desk_agent",
            "enableTrace": True,
            "endSession": False,
            "foundationModel": self.foundational_model,
            "instruction": (
                "You are the Front Desk Agent. Your primary goal is to provide detailed, accurate, and helpful information "
                "about our company and orders. Your responsibility is to talk to the user to understand their needs and "
                "then relay the information to the Order Support Agent and Marketing Agent. "
            ),
            "agentCollaboration": "SUPERVISOR_ROUTER",
            "sessionId": self.session_id,
            "collaboratorConfigurations": [
                {
                    "collaboratorInstruction": "Use to answer questions about the company.",
                    "collaboratorName": "marketing_agent",
                    "relayConversationHistory": "TO_COLLABORATOR"
                },
                {
                    "collaboratorInstruction": "Use to answer questions about the company.",
                    "collaboratorName": "order_support_agent",
                    "relayConversationHistory": "TO_COLLABORATOR"
                },
                {
                    "collaboratorInstruction": "Use to answer questions about products the company is selling.",
                    "collaboratorName": "product_support_agent",
                    "relayConversationHistory": "TO_COLLABORATOR"
                }
            ],
            "collaborators": [
                self.order_support_agent.agent_request_params(as_collaborator=True),
                self.marketing_agent.agent_request_params(as_collaborator=True),
                self.product_support_agent.agent_request_params(as_collaborator=True)
            ],
        }
        return basic_config

    def prepare_input(self, input_text: str) -> dict:
        params = self.agent_request_params()
        params["inputText"] = input_text

        return params
