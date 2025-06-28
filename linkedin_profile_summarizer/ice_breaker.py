from langchain.prompts.prompt import PromptTemplate
from langchain_groq import  ChatGroq
from langchain.chains import LLMChain
from dotenv import load_dotenv
from linkedin import Linkedin_scraper
import os


load_dotenv()

summary_template = """
Given the linkedin information {information} about a person, i want you to create:
1. A short summary
2. Two interesting facts about them
3. Their career history in a line
4. Their most important skills (That are either certified or displayed through their work) 
"""

summary_prompt_template=PromptTemplate(
    input_variables=['information'], template=summary_template
)
llm = ChatGroq(temperature=0, model='llama3-70b-8192')

chain = summary_prompt_template | llm

linkedin_data = Linkedin_scraper.scrape_linkedin_profile(linkedin_profile_url='https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json')

import json
print("Scraped LinkedIn Data:")
print(json.dumps(linkedin_data, indent=2))

res = chain.invoke(input={"information": linkedin_data})

print(res)