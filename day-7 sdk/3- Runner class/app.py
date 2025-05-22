from openai.agents import AssistantAgent, Task
from openai.agents.run import Runner

# Define the agent
agent = AssistantAgent(name="HelperAgent")

# Define the task for the agent
task = Task(instructions="Write a Python function to calculate factorial of a number.")

# Pass the agent into the Runner
runner = Runner(agent=agent)

# Execute the task using the Runner
run = runner.run(task)

# Output the result
print(run.output)

from dataclasses import dataclass
from typing import List

@dataclass
class Agent:
    instructions: str
    tools: List[str]

class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str) -> str:
        print(f"Executing with instructions: {agent.instructions}")
        print(f"Tools available: {agent.tools}")
        return f"Response to: {user_prompt}"

agent = Agent(instructions="You are a travel planner", tools=["weather_api"])
response = Runner.run(agent, "Plan a trip to Paris")
print(response)