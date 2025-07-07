from dotenv import load_dotenv
from langchain import hub
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent,AgentExecutor
from langchain_experimental.tools import PythonREPLTool
# The pytohnREPLTool gives the agent the power to write and execute
#python code in the interpreter. This is very cool but highly dangerous in production

load_dotenv()

def main():
    print("Start...")

    instructions = """
    You are an agent designed to write and execute python code to answer questions
    You have access to a python REPL, which you can use to execute python code. 
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the questions.
    Even if you might know the answer to the question without running the code, 
    you should still run the code to get the answer.
    if it does not seem that you can write the code to answer the question, 
    just return 'I dont know' as the answer.

    """
    base_prompt=hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    agent = create_react_agent(
        prompt = prompt,
        llm=ChatGroq(temperature=0, model='llama3-70b-8192'),
        tools = tools,
    )
    agent_executer = AgentExecutor(agent=agent, tools = tools, verbose=True)
    agent_executer.invoke(
        input= {
            "input": """
            create a text file containing 5 sentences to roast me and make 
            my life miserable
            """
        }
    )

main()

