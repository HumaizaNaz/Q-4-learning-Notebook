from dataclasses import dataclass
from typing import TypeVar, Generic, List, Callable
import re

# Generic type for context
TContext = TypeVar("TContext")

# Mock SDK simulating external APIs
class SDK:
    def get_weather(self, city: str) -> str:
        """Mock weather API that returns weather for a city."""
        return f"The weather in {city} is sunny with a temperature of 25°C."

    def get_hotels(self, city: str, budget: int) -> str:
        """Mock hotel API that suggests hotels based on the budget."""
        if budget >= 100:
            return f"Available budget hotels in {city}: Hotel Star, Hotel Moon."
        return f"No hotels found in {city} for the budget of ${budget}."

# Generic Agent class
@dataclass
class Agent(Generic[TContext]):
    instructions: str | Callable[[TContext], str]  # Static or dynamic instructions
    tools: List[str]  # List of tools (e.g., weather_api, hotel_api)
    context: TContext  # Generic context (can be string or dict)
    model: str = "gpt-4"  # Default model

    def __call__(self, user_input: str) -> str:
        """Makes the agent callable like a function."""
        instructions = self.instructions(self.context) if callable(self.instructions) else self.instructions
        return f"{instructions}: Processing '{user_input}'"

# Runner class for handling user input and executing tasks
class Runner:
    @classmethod
    def run(cls, agent: Agent, user_prompt: str, sdk: SDK) -> str:
        """Runs the agent with the given user prompt and SDK tools."""
        print(f"Running with tools: {agent.tools}")
        
        # Handle dynamic/static instructions
        instructions = agent.instructions(agent.context) if callable(agent.instructions) else agent.instructions  # noqa: F841
        
        # Extract city and budget from the user prompt
        city_match = re.search(r"\b(Karachi|Lahore|Paris|London)\b", user_prompt, re.IGNORECASE)
        budget_match = re.search(r"\$(\d+)", user_prompt)
        
        city = city_match.group(0) if city_match else "unknown city"
        budget = int(budget_match.group(1)) if budget_match else 100
        
        # If the prompt mentions weather
        if "weather" in user_prompt.lower() or "mausam" in user_prompt.lower():
            weather = sdk.get_weather(city)
            return f"{agent(user_prompt)}\nWeather Info: {weather}"
        
        # If the prompt mentions a trip
        elif "trip" in user_prompt.lower():
            weather = sdk.get_weather(city)
            hotels = sdk.get_hotels(city, budget)
            return f"{agent(user_prompt)}\nWeather Info: {weather}\nHotel Info: {hotels}"
        
        return agent(user_prompt)

# Dynamic instruction generator
def dynamic_instructions(context: dict) -> str:
    """Creates dynamic instructions based on context."""
    user = context.get("user", "Guest")
    budget = context.get("budget", 1000)
    return f"You are a travel planner for {user} with a budget of ${budget}."

# Main execution function
def main():
    sdk = SDK()
    
    # Agent with static instructions
    agent_static = Agent[str](
        instructions="You are a travel planner",
        tools=["weather_api", "hotel_api"],
        context="The user is a tourist",
        model="llama-3"
    )
    
    print("Static Agent Test:")
    response1 = Runner.run(agent_static, "What is the weather like in Karachi?", sdk)
    print(response1)
    print("\n")
    
    response2 = Runner.run(agent_static, "Plan a trip to Paris with a $200 budget", sdk)
    print(response2)
    print("\n")
    
    # Agent with dynamic instructions
    agent_dynamic = Agent[dict](
        instructions=dynamic_instructions,
        tools=["weather_api", "hotel_api"],
        context={"user": "Ali", "budget": 200}
    )
    
    print("Dynamic Agent Test:")
    response3 = Runner.run(agent_dynamic, "Plan a trip to Lahore with a $150 budget", sdk)
    print(response3)

if __name__ == "__main__":
    main()
