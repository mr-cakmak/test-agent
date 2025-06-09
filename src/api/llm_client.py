import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Get the project root directory (two levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

#this requires to have OPENAI_API_KEY env variable in .env file
model = ChatOpenAI(model="gpt-4o", temperature=0)
