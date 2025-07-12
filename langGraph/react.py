from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

load_dotenv()

@tool
def triple(num:float) -> float:
    """
    param num: a number to triple
    returns the triple of the input number
    """
    return float(num) * 3

tools = [TavilySearch(max_results=5), triple]

llm = ChatGroq(temperature=0, model="llama3-70b-8192").bind_tools(tools)

