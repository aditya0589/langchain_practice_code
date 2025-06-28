from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub


load_dotenv()

def lookup(name: str) -> str:
    llm = ChatGroq(temperature = 0, model='llama3-70b-8192')

    template = """
    given the full name of the person {full_name_person}, i want you
    to get me a link to their linkedin profile, your answer should only
    contain a URL
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=['full_name_person']
    )
    tools_for_agent = [
        Tool("Crawl Google 4 linkedin profile page",
             func = "?",
             description="useful for when you want to get the Linkedin Page URL"
             )
    ]
    react_prompt = hub.pull('hwchase17/react') # Harrsion chase 's react agent

    
