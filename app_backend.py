from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import run_research_pipeline
app = FastAPI()

class TopicRequest(BaseModel):
    topic : str
    tavily_api_key:str
    llm_api_key:str


@app.get('/')
def health():
    return {'message':'api working'}

@app.post('/research')
def research(data :TopicRequest):

    result = run_research_pipeline(data.topic,
    tavily_api_key = data.tavily_api_key,
    llm_api_key = data.llm_api_key)

    return {
        "report":result['report'],
        "feedback":result['feedback']
    }