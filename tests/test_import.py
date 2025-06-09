from src.api.llm_client import model
from langchain_core.messages import HumanMessage

response = model.invoke([HumanMessage(content="Hello, just testing!")])
print(response.content)
