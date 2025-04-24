import uuid
from abc import ABC


DEFAULT_FOUNDATIONAL_MODEL = "eu.amazon.nova-lite-v1:0"


class NonCollaboratingAgent(ABC):
    def __init__(self, instructions: str, foundational_model: str = None, session_id: str = None, name: str = None):
        self.foundational_model = foundational_model if foundational_model else DEFAULT_FOUNDATIONAL_MODEL
        self.session_id = session_id if session_id else str(uuid.uuid4())
        self.instructions = instructions
        self.action_group = None
        self.knowledge_base = None
        self.name = name

    def agent_request_params(self, as_collaborator: bool = False) -> dict:
        basic_config = {
            "agentName": self.name,
            "enableTrace": True,
            "endSession": False,
            "foundationModel": self.foundational_model,
            "instruction": self.instructions,
            "agentCollaboration": "DISABLED",
            "sessionId": self.session_id,
        }
        if self.action_group:
            basic_config["actionGroups"] = [{
                "actionGroupName": self.action_group["name"],
                "actionGroupExecutor": {
                    "lambda": self.action_group["executor"]
                },
                "apiSchema": {
                    "payload": self.action_group["payload"]
                },
                "description": self.action_group["description"]
            }]
        if self.knowledge_base:
            basic_config["knowledgeBases"] = [
                self.knowledge_base
            ]

        if as_collaborator:
            basic_config.pop("enableTrace", None)
            basic_config.pop("endSession", None)
            basic_config.pop("sessionId", None)
            # basic_config.pop("agentName", None)

        return basic_config

    def prepare_input(self, input_text: str) -> dict:
        params = self.agent_request_params()
        params["inputText"] = input_text

        return params