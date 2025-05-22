from dataclasses import dataclass
from typing import List, Union, Callable

@dataclass
class Agent:
    instructions: Union[str, Callable[[dict], str]]
    tools: List[str]
    model: str = "gpt-4"

def dynamic_instructions(context: dict) -> str:
    user = context.get("user", "Guest")
    budget = context.get("budget", 1000)
    return f"You are a travel planner for {user} with a budget of ${budget}."

agent_static = Agent(
    instructions="You are a travel planner.",
    tools=["flight_api"]
)

agent_dynamic = Agent(
    instructions=dynamic_instructions,
    tools=["flight_api"]
)

context = {"user": "Ali", "budget": 500}

for agent in [agent_static, agent_dynamic]:
    if callable(agent.instructions):
        print(agent.instructions(context))
    else:
        print(agent.instructions)
