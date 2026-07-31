from config import get_llm
from docx import Document
from .starting import State
from pydantic import BaseModel, Field
from langchain.messages import AIMessage, HumanMessage, SystemMessage




llm = get_llm()

class taloried_recommendations(BaseModel):
    skills: str = Field(description="find the best skills matching the between my resume details and  requirements of the company and place top to bottom on the basis skills mentioned in requirement")
    project: str = Field(description="find the best projects matching the between my resume details requirements of the company and place top to bottom on the basis projects mentioned in requirement")
    all_gaps: str = Field(description="find the gaps in skills and projects and experience from the company requirements ")

def resume_evaluator(state:State):
    doc = Document("Priyanshu_Harsana_Resume.docx")

    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    text = "\n".join(full_text)
    print(text)
    system=SystemMessage(content=
        "You are a resume-building specialist.\n"
        "1. Analyze the job requirements provided.\n"
        "2. Compare them against the candidate's resume.\n"
        "3. List matching skills and projects.\n"
        "4. List missing or weak skills/projects the candidate should improve or add."
    )
    human= HumanMessage(
        content=f"""
        resume details: {text}/n
        job requirements
        company_name:{state["company_name"]},
        requirement_title:    {state["requirement_title"]},
            {state["requirement_skill"]},
            {state["requirement_responsibilities"]}
            """
    )
    llm_structure = llm.with_structured_output(taloried_recommendations)
    response = llm_structure.invoke([system,human])
    return response