from typing import List

# ✅ Part 1: Simple Agent without Tools
from dataclasses import dataclass

# Agent class sirf instructions leta hai
@dataclass
class Agent:
    instructions: str

# Runner class ka classmethod run agent ko handle karta hai
class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str) -> str:
        print(f"Running with instructions: {agent.instructions}")
        return f"Response to: {user_prompt}"

# Agent ka object banaya gaya
agent = Agent(instructions="You are a helpful assistant")

# Runner ke zariye agent ko run kiya
response = Runner.run(agent, "What's the weather in Karachi?")
print(response)
# ✅ Part 2: Agent with Tools
# from dataclasses import dataclass
# from typing import List

# Ab Agent ke paas instructions ke sath tools bhi hain
@dataclass
class Agent:
    instructions: str
    tools: List[str]

# Runner class instructions aur tools dono handle karti hai
class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str) -> str:
        print(f"Executing with instructions: {agent.instructions}")
        print(f"Tools available: {agent.tools}")
        return f"Response to: {user_prompt}"

# Agent ka object banaya gaya with tools
agent = Agent(instructions="You are a travel planner", tools=["weather_api"])

# Runner ke zariye agent ko run kiya
response = Runner.run(agent, "Plan a trip to Paris")
print(response)
