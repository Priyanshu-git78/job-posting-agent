from langchain_community.document_loaders import WebBaseLoader
from langchain_core.globals import set_debug
import os
import pandas as pd
from pydantic import BaseModel,Field
from typing import TypedDict, Literal
from dotenv import load_dotenv
from config import get_llm

load_dotenv()

# creating class for shared the state passed  all langgraph nodes during workflow exceution.
llm=get_llm()


# debug the langchian process
set_debug(True)


class State(TypedDict):
    user_input:str
    link : str 
    page_content:str
    company_name:str
    requirement_title:str
    requirement_skill :str
    requirement_responsibilities:str
    my_resume_rank_against_it :str
    my_shortcoming :str
    matching_skills: str
    matching_projects: str 
    all_gaps: str
    rank:str
    summary:str
    


class companydetails(BaseModel):
    company_name:str
    requirement_title:str
    requirement_skill :str
    requirement_responsibilities:str

class message_pattern_identifier(BaseModel):
    message_intent:Literal['page_content','link']=Field(..., description="classify whether user is giving 'link' or 'page_content'")
    reason: str



# Duckduckgosearch help getting the output form the url
def route_start(state: State) -> str:
    user_input = state["user_input"].strip()

    if user_input.startswith(("http://", "https://")):
        return "search"

    # crude heuristic: if it's short and looks like prose/labeled text, treat as content
    if len(user_input) > 0:
        return "company_details_extractor"

    raise ValueError("Empty user_input provided.")

def odx_editor(state:State):
    """"""
    df=pd.DataFrame([state])
    print(df)
    write_header = not os.path.exists("details.csv")
    df.to_csv("details.csv", mode="a",header=write_header,index=False)
    return state

def search_url(state:State):
    """Fetch the raw page content from the job posting link."""
    loader = WebBaseLoader(state["user_input"])
    docs = loader.load()
    page_text = "\n".join(d.page_content for d in docs)
    return {"link": state["user_input"],"page_content": page_text}  # add this key to State if you keep this approach



def company_details_extractor(state:State)-> dict:
    content = state.get("page_content") or state["user_input"]
    """this function uses LLM get the company and job details """
    messages=[
        {'role' :'user',"content": f"You job is get the company and job details and provide summary of it 1. summary should concise and accurate to the :\n{content}"}
    ]

    llm_structure=llm.with_structured_output(companydetails)
    response=llm_structure.invoke(messages)  
    return response


