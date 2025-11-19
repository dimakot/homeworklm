import os
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())

model = OpenAILike(
    id="Qwen/Qwen3-Next-80B-A3B-Instruct",
    name="Foundation model",
    provider= "cloud.ru",
    support_native_structured_outputs=True,
    
)

agent = Agent(
    model = model,
    name="Протоиерей Метрофан",
    tools = [
        DuckDuckGoTools(),
    ],
    instructions="Ты священник русской православной церкви (Батюшка, святой отец, sugar daddy). Твоя задача помогать пользователю искать в интернете молитвы и кооректировать их под нужды пользователя",
    markdown=True,
    stream=True,
)

agent.print_response(input="[Хочу помолиться за попу инстасамки]")