from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
# the node which is going to execute the tool. if the last message is a valid AI
#message with a tool call, then it is going to execute the tool. 

from react import llm, tools # imports from the react.py file

load_dotenv()
SYSTEM_MESSAGE = """
You are a helpful assistant that uses tools to answer questions
"""

def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning node
    """
    response = llm.invoke([
        {"role": "system", "content": SYSTEM_MESSAGE},
        *state["messages"]
    ])
    return MessagesState(messages=state["messages"] + [response])


tool_node = ToolNode(tools)


