from typing import TypeVar, Generic

TContext = TypeVar("TContext")

class Agent(Generic[TContext]):
    def __init__(self, instructions: str, context: TContext):
        self.instructions = instructions
        self.context = context

# String context
agent1 = Agent[str](instructions="Be a teacher", context="User is a student")
print(agent1.context)

# Dict context
agent2 = Agent[dict](instructions="Be a planner", context={"user": "Ali", "budget": 500})
print(agent2.context)