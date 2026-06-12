from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_llm(llm_api_key):
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0,
        mistral_api_key=llm_api_key
    )

#1st agent

def search_agent(
    llm_api_key,
    tavily_api_key
):

    llm = get_llm(llm_api_key)
    @tool
    def search_tool(query:str):

        """Search the web using Tavily"""

        return web_search.invoke({
            'query':query,
            'tavily_api_key':tavily_api_key
        })

    return create_agent(

        model=llm,

        tools=[search_tool]
    )

#2nd agent

def reader_agent(llm_api_key):
    llm = get_llm(llm_api_key)
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


writer_prompt = ChatPromptTemplate.from_messages([
("system", "You are an expert research writer. Write clear, structured and insightful reports."),
("human", """
 Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
 """),
])

def writer_chain(llm_api_key):

    llm = get_llm(llm_api_key)

    return writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
("system", "You are a sharp and constructive research critic. Be honest and specific."),
("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""),
])

def critic_chain(llm_api_key):

    llm = get_llm(llm_api_key)

    return critic_prompt | llm | StrOutputParser()
