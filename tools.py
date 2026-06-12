from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

def get_tavily_client(tavily_api_key):

    return TavilyClient(api_key=tavily_api_key)


@tool
def web_search(query : str, tavily_api_key:str) ->str:

    """Search the web for recent and reliable information.
      Returns Title ,
      URL and snippets."""
    
    tavily = get_tavily_client(tavily_api_key)

    result = tavily.search(query=query , max_results = 5)

    out = []

    for r in result['results']:
        out.append(
                   f"Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}\n"
                   )
    return "\n----------------------------------------\n".join(out)

@tool
def scrape_url(url  :str)->str:
    """Scrape and return clean text content from given url for deeper reading."""

    try:

        resp = requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"}) 
        soup = BeautifulSoup(resp.text,"html.parser")

        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()

        return soup.get_text(separator = " ", strip=True)[:3000]
    
    except Exception as e:

        return f"Could not scrape URL : {str(e)}"

    