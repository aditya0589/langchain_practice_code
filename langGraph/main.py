from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, END
from node import run_agent_reasoning, tool_node

load_dotenv()

AGENT_REASON = "agent reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    if not state['messages'][-1].tool_calls:
        return END

    return ACT
flow = StateGraph(MessagesState)
flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)

flow.add_conditional_edges(AGENT_REASON, should_continue, {
    END:END,
    ACT:ACT
})

flow.add_edge(ACT, AGENT_REASON)
app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")
# the draw_mermaid_png generates a graph visualization of your LangGraph workflow.
#Uses Mermaid.js syntax under the hood to render a PNG image of the graph.
#Saves the image as flow.png.



res = app.invoke({"messages": [HumanMessage(content="First, find the recent five weathers in Tokyo using search and print it. Then, triple the temperature value you find."
)]})
print(res["messages"][-1].content)
