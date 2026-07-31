from .starting import route_start, search_url, company_details_extractor, odx_editor,State
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from uuid import uuid4
from .resume_builder import resume_evaluator



def graph_main():
    #initalize the stategraph of langgraph
    graph_builder = StateGraph(State)


    # nodes of langgraph
    graph_builder.add_node("search",search_url)
    graph_builder.add_node("company_details_extractor",company_details_extractor)
    graph_builder.add_node("odx_editor",odx_editor)
    graph_builder.add_node("evaluator",resume_evaluator)

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
    graph_builder.add_edge("company_details_extractor", "evaluator")
    graph_builder.add_edge("evaluator","odx_editor")
    graph_builder.add_edge("odx_editor",END)

    checkpointer=InMemorySaver()
    graph=graph_builder.compile(checkpointer=checkpointer)
    config = {'configurable':{"thread_id":uuid4()}}
    graph.get_graph().draw_mermaid_png(output_file_path="technicals.png")
    return graph,config
