from agents import search_agent,reader_agent,writer_chain,critic_chain , get_llm
import re

def run_research_pipeline(topic :str,
                          tavily_api_key :str,
                          llm_api_key)->str:


    state = {}
    #search agent
    print("\n"+" ="*55)
    print("step-1 - search agent is working ...")
    print("\n"+" ="*55)

    search_result = search_agent(llm_api_key,tavily_api_key).invoke({
        "messages" : [("user",f"Find recent, reliable and detailed information about : {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content
    print("\n Search Result \n",state["search_results"])
    print("\n"+" ="*55)

    urls = re.findall(
    r'https?://\S+',
    state['search_results']
    )
# step 2
    print("step-2 - Reader agent is scraping top resources ...")
    print("\n"+" ="*55)

    for url in urls[:3]:

        reader_result = reader_agent(
        llm_api_key
    ).invoke({

        "messages":[(

            "user",

            f"""
            Topic: {topic}

            Search Results:
            {state['search_results'][:1000]}

            Carefully scrape and analyze this URL:

            {url}

            Extract:
            - important findings
            - statistics
            - technical insights
            - useful information related to the topic
            """
        )]
    })
    if urls:
        state['reader_result'] = reader_result['messages'][-1].content
    else:
        state['reader_result'] = "No URLs found in search results."
    print("\n Scrapped Content \n",state["reader_result"])
    print("\n"+" ="*55)

    # step 3

    print("\n"+" ="*55)
    print("step-3 - writer is drafting the report ...")
    print("\n"+" ="*55)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['reader_result']}" 
    )

    state['report']=writer_chain(llm_api_key).invoke({
        "topic":topic,
        'research':research_combined
    })

    print("\n Final Report \n",state["report"])
    print("\n"+" ="*55)

    #critic report 

    print("\n"+" ="*55)
    print("step-4 -  Critic is Reviewing ...")
    print("\n"+" ="*55)

    state['feedback']=critic_chain(llm_api_key).invoke({
        "report":state['report']
    })

    print("\n Critic Report \n",state["feedback"])
    print("\n"+" ="*55)

    return state

if __name__ == "__main__":

    topic = input("\n Enter a research topic ... \n")
    
    run_research_pipeline(topic)