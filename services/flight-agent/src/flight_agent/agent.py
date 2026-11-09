from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI


import os 

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatOpenAI(
    api_key=os.environ["MODEL_API_KEY"],
    base_url=os.environ.get("MODEL_BASE_URL"),
    model=os.environ.get("MODEL", "arillm/qwen_medium"),
    temperature=0,
)
agent = create_deep_agent(model=model, tools=[get_weather], system_prompt="Sei il Flight Agent: cerchi, confronti e selezioni soluzioni di volo e treno.")



