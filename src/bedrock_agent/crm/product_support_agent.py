import boto3
from botocore.exceptions import ClientError

from bedrock_agent.crm.non_collaborating_agent import NonCollaboratingAgent

KNOWLEDGE_BASE_ID = "E3KSHKTHEL"

class ProductSupportAgent(NonCollaboratingAgent):
    def __init__(self, aws_region: str, knowledge_base_id: str, foundational_model: str = None, session_id: str = None):
        instructions = (
            "You are the Product Support Agent. Your primary goal is to provide detailed, accurate, and helpful information "
            "about the products. Use only the information from the provided AWS knowledge base. If the information is not available, "
            "do not make up information, tell that you do not know."
        )
        super().__init__(instructions, foundational_model, session_id, name="product_support_agent")
        self.aws_region = aws_region
        self.knowledge_base_id = KNOWLEDGE_BASE_ID

        # Initialise the KnowledgeBase
        self._add_knowledge_base()
        

    def _add_knowledge_base(self):
        # Add the knowledge base to the agent
        self.knowledge_base = {
            "description": "Knowledge base for product support, contains information about products that we sell.",
            "knowledgeBaseId": self.knowledge_base_id
        }
