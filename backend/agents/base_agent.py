import asyncio
from events.event_manager import event_manager
from datetime import datetime

class BaseAgent:
    # def __init__(self, name: str):
    #     self.name = name
    agent_name = "BASE_AGENT"

    async def run(self, state):
        raise NotImplementedError("Subclasses must implement this method")

    async def emit_event(self, payload):
        print("Agent Name:", self.agent_name)
        event = {
            "agent": self.agent_name,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            **payload
        }
        await event_manager.broadcast(event)