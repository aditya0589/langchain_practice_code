from dotenv import load_dotenv
from langchain import hub
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents import create_csv_agent
from langchain.tools import Tool
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
    python_agent = create_react_agent(
        prompt = prompt,
        llm=ChatGroq(temperature=0, model='llama3-70b-8192'),
        tools = tools,
    )
    python_agent_executer = AgentExecutor(agent=python_agent, tools = tools, verbose=True)
    # python_agent_executer.invoke(
    #     input= {
    #         "input": """
    #         create a text file containing 5 sentences to roast me and make 
    #         my life miserable
    #         """
    #     }
    # )

    # csv_agent = create_csv_agent(
    #     llm = ChatGroq(temperature=0, model="llama3-70b-8192"),
    #     path="episode_info.csv",
    #     verbose=True,
    #     allow_dangerous_code=True,
    # )
    # csv_agent.invoke(
    #     input={"input": "How many episodes does each season have?"}
    # )
    csv_agent_executer: AgentExecutor = create_csv_agent(
        llm = ChatGroq(temperature=0, model="llama3-70b-8192"),
        path="episode_info.csv",
        verbose=True,
        allow_dangerous_code=True, 
    )

    tools = [
        Tool(
            name = "Python Agent",
            func = python_agent_executer.invoke,
            description = """
            useful when you need to transform natural language to python and execute
            the python code. return results of the code execution.
            DOES NOT ACCEPT CODE AS INPUT
            """
        ),
        Tool(
            name = "CSV Agent",
            func = csv_agent_executer.invoke,
            description = """
            useful when you need to return a query on a CSV file, over the 
            episode_info.csv file. takes the entire query as an input and returns 
            the results after certain pandas calculations. 
            """
        )
    ]
    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt = prompt,
        llm = ChatGroq(temperature=0, model="llama3-70b-8192"),
        tools = tools,
    )
    grand_agent_executer = AgentExecutor(agent = grand_agent, tools = tools, verbose = True,
                                         allow_dangerous_code = True)
    
    print(
        grand_agent_executer.invoke(
            {
                "input": "which season has the most episodes?"
            }
        )
    )

main()
