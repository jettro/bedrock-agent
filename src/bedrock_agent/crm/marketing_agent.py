import uuid
from abc import ABC

from bedrock_agent.crm.non_collaborating_agent import NonCollaboratingAgent


class MarketingAgent(NonCollaboratingAgent):
    def __init__(self, foundational_model: str = None, session_id: str = None):
        instructions = (
            "You are the Marketing Agent. Your primary goal is to provide detailed, accurate, and helpful information "
            "about our company. You can make up everything you want, but make sure it is believable."
        )
        super().__init__(
            instructions=instructions,
            foundational_model=foundational_model,
            session_id=session_id,
            name="marketing_agent"
        )
