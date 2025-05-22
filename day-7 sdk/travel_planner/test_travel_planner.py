import pytest
from travel_planner_agent import Agent, Runner, SDK, dynamic_instructions

# Fixtures
@pytest.fixture
def sdk():
    """Provides a mock SDK object for testing."""
    return SDK()

@pytest.fixture
def static_agent():
    """Provides an agent with static instructions."""
    return Agent[str](
        instructions="You are a travel planner",
        tools=["weather_api", "hotel_api"],
        context="The user is a tourist",
        model="llama-3"
    )

@pytest.fixture
def dynamic_agent():
    """Provides an agent with dynamic instructions."""
    return Agent[dict](
        instructions=dynamic_instructions,
        tools=["weather_api", "hotel_api"],
        context={"user": "Ali", "budget": 200}
    )

# ✅ Test 1: Static agent - weather prompt
def test_static_agent_weather(static_agent, sdk):
    """Tests the static agent with a weather-related prompt."""
    response = Runner.run(static_agent, "What is the weather like in Karachi?", sdk)
    assert "You are a travel planner" in response
    assert "The weather in Karachi is sunny" in response

# ✅ Test 2: Static agent - trip planning
def test_static_agent_trip_plan(static_agent, sdk):
    """Tests the static agent with a trip planning prompt."""
    response = Runner.run(static_agent, "Plan a trip to Paris with a $200 budget", sdk)
    assert "You are a travel planner" in response
    assert "The weather in Paris is sunny" in response
    assert "Hotel Star, Hotel Moon" in response

# ✅ Test 3: Dynamic agent - trip planning
def test_dynamic_agent_trip_plan(dynamic_agent, sdk):
    """Tests the dynamic agent with a trip planning prompt."""
    response = Runner.run(dynamic_agent, "Plan a trip to Lahore with a $150 budget", sdk)
    assert "You are a travel planner for Ali with a budget of $200" in response
    assert "The weather in Lahore is sunny" in response
    assert "Hotel Star, Hotel Moon" in response

# ✅ Test 4: Dynamic agent is callable
def test_callable_agent(dynamic_agent):
    """Tests that the dynamic agent is callable like a function."""
    response = dynamic_agent("Test input")
    assert "You are a travel planner for Ali with a budget of $200" in response
