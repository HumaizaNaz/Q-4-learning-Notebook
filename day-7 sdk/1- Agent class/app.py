from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Agent:
    instructions: str
    tools: List[str]
    model: str = "gpt-4"
    max_iterations: Optional[int] = None

# Create an agent instance
agent = Agent(
    instructions="You are a travel planner.",
    tools=["flight_api", "hotel_api"],
    model="llama-3"
)

print(agent)

#What is agentic AI?
class AgenticAI:
    def __init__(self, role):
        self.role = role

    def execute_task(self, user_input):
        print(f"Role: {self.role}")
        print(f"Processing user input: {user_input}")
        return f"Task completed: Planned a trip based on {user_input}"

# Instantiate and execute
agent = AgenticAI("Travel Planner")
print(agent.execute_task("Plan a 3-day trip to Paris"))
