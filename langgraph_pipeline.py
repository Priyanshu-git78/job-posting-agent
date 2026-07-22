from langgraph.graph import MessagesState, StateGraph, START,END
from typing import TypedDict
from pydantic import BaseModel

from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.document_loaders import WebBaseLoader
from langchain.chat_models import init_chat_model
# data manipulation
import pandas as pd
import numpy as np
import os
#UUId 
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()
llm = init_chat_model(
    model= "gemma-3-12b",
    openai_api_base ="http://localhost:8005/v1",
    openai_api_key= "MUP78",
    model_provider ="openai",
    temperature = 0.0
)

tool = DuckDuckGoSearchRun()

class vacancy_details(BaseModel):
    company: str
    Location :str
    Job_ID : str
    position : str
    resposibilities:str
    raw_search:str



class State(TypedDict):
    file_path:str
    links : list[str]
    company: list[str]
    Location :list[str]
    Job_ID : list[str]
    position : list[str]
    resposibilities:list[str]
    raw_search:list[str]

def websearch(state:State):
    links=state['links']
    results=list()
    for link in links: 
        try:
            docs = WebBaseLoader(link).load()
            results.append(docs[0].page_content)
        except Exception as e:
            print(f"ERROR: {e}")
        
    return {"raw_search": results}

def odx_editor(state:State):
    df =pd.read_excel(state['file_path'],engine="odf")
    links=df['links'].dropna().tolist()
    print(links)
    return {"links":links}

def llm_structure_output(state:State):
    raw_data=state['raw_search']
    llm_svo=llm.with_structured_output(vacancy_details,method="function_calling")
    responses=[]
    for raw in raw_data:
        response =llm_svo.invoke([
            {'role':'system','content':f"You are data cleaning and expert you are required to give structured ouput'+{raw}"}])
        responses.append(response)
    return {'company':responses.get('company'),'Location':responses['Location'],'resposibilities':responses['resposibilities'],'raw_search':responses['raw_search']}

# def edit_excel(state:State):
#     state[]



def main(excel_path):
    graph_builder = StateGraph(State)

    graph_builder.add_node("odx_editor",odx_editor)
    graph_builder.add_node("websearch",websearch)
    graph_builder.add_node("llm_structure_output",llm_structure_output)
    graph_builder.add_edge(START,'odx_editor')
    graph_builder.add_edge('odx_editor','websearch')
    graph_builder.add_edge("websearch","llm_structure_output")
    graph_builder.add_edge("llm_structure_output",END)
    checkpointer= InMemorySaver()
    graph =graph_builder.compile(checkpointer=checkpointer)
    graph.get_graph().draw_mermaid_png(output_file_path="technical.png")
    config = {'configurable':{"thread_id":uuid4()}}
    result= graph.invoke({'file_path':excel_path}, config=config)
    return result

if __name__=="__main__":
    result=main(excel_path=r"/mnt/hdd/Job Applications/Applications list.ods")
    print(result)