from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.globals import set_debug, set_verbose
import os
import pandas as pdlink
from pydantic import BaseModel,Field
from typing import TypedDict,Annotated, Literal
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from uuid import uuid4
import streamlit as st
# creating class for shared the state passed  all langgraph nodes during workflow exceution.

llm=init_chat_model(
    model="Qwen/Qwen3-4B",
    openai_api_base="http://localhost:8005/v1",
    openai_api_key="pranshu123",
    model_provider="openai",
    temperature=0.0
)


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
    print(response)  
    return response


#initalize the stategraph of langgraph
graph_builder = StateGraph(State)


# nodes of langgraph
graph_builder.add_node("search",search_url)
graph_builder.add_node("company_details_extractor",company_details_extractor)


#conditional 
graph_builder.add_conditional_edges(
    START,
    route_start,
    {
        "search": "search",
        "company_details_extractor": "company_details_extractor",
    },
)

graph_builder.add_edge("search", "company_details_extractor")
graph_builder.add_edge("company_details_extractor", END)


checkpointer=InMemorySaver()
graph=graph_builder.compile(checkpointer=checkpointer)
config = {'configurable':{"thread_id":uuid4()}}
graph.get_graph().draw_mermaid_png(output_file_path="technicals.png")

import streamlit as st




user_input = st.chat_input("Enter job details or a job posting link:")

if user_input:
    with st.spinner("Processing..."):
        try:
            final_state = None
            for event in graph.stream(
                {"user_input": user_input},
                config=config,
                stream_mode="updates",
            ):
                st.write(event)   # show each node's output as it streams in
                final_state = event

            st.success("Done")
            if final_state:
                st.json(final_state)

        except Exception as e:
            st.error(f"Something went wrong: {e}")