from config import get_llm
from docx import Document
from .starting import State
from pydantic import BaseModel, Field
from langchain.messages import AIMessage, HumanMessage, SystemMessage




llm = get_llm()

class taloried_recommendations(BaseModel):
    skills: str = Field(description="List the candidate's skills that match the company's job requirements, "
            "ordered from strongest match to weakest, based on how closely each skill "
            "aligns with the specific skills mentioned in the job requirements.")
    project: str = Field(description="List the candidate's projects that best demonstrate the required skills "
            "and responsibilities, ordered from most relevant to least relevant, based "
            "on the job requirements.")
    all_gaps: str = Field(description="List all gaps between the candidate's resume and the job requirements — "
            "including missing skills, missing or insufficient project experience, and "
            "missing years of relevant experience.")

class rank_summary(BaseModel):
    rank: int = Field(description="A numeric score between 0 and 1 representing the estimated likelihood of the "
            "candidate being selected, based on how well their skills, projects, and experience "
            "match the company's requirements. 0 = no chance, 1 = perfect match.")
    summary:str =Field(description="A concise, actionable summary explaining what the candidate should add, improve, "
            "or emphasize in their resume to maximize their chances of selection, based on the "
            "identified gaps and matching strengths.")



def resume_evaluator(state:State):
    doc = Document("Priyanshu_Harsana_Resume.docx")

    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    text = "\n".join(full_text)
    print(text)
    system=SystemMessage(content=
        "You are a resume-building specialist. follow these steps\n"
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
        requirement_skills:   {state["requirement_skill"]},
        requirement_responsibilites :{state["requirement_responsibilities"]}
        """
    )
    llm_structure = llm.with_structured_output(taloried_recommendations)
    response = llm_structure.invoke([system,human])
    return {
        "resume_text": text,
        "matching_skills": response.skills,
        "matching_projects": response.project,
        "all_gaps": response.all_gaps,
    }

def summary(state:State):
    company_name=state["company_name"]
    requirement_title=    state["requirement_title"]
    requirement_skills=  state["requirement_skill"]
    requirement_responsibilites =state["requirement_responsibilities"]
    doc = Document("Priyanshu_Harsana_Resume.docx")
    
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    text = "\n".join(full_text)

    skills_match= state["matching_skills"]
    project_match=state["matching_projects"]
    all_gaps=   state["all_gaps"]
    messages =[SystemMessage(content=
    "You are a resume analyzer analyst. Your job is to analyze the company's \n"
    "job requirements against the candidate's resume. Identify matching skills \n"
    "and projects, list missing or weak skills/projects, and rank and provide the summary to the candidate \n"
    "based on overall fit.\n"
    ),
    HumanMessage(content=f"""
    company requirements details:
    {requirement_title},requirement:{requirement_skills},responsbilities{requirement_responsibilites}
    candiadate["resume"]
    matching_profile details:
    skills :{skills_match}
    projects:{project_match}
    all_gaps : {all_gaps}

    """)]
    llm_structure = llm.with_structured_output(rank_summary)
    response = llm_structure.invoke(messages)
    return response

def resumeEdit(state:State):
    doc = Document("Priyanshu_Harsana_Template.docx") #[AI/ML Engineer with 2+ years of experience building and deploying production-grade Machine Learning , Generative AI and Python-based solutions across the full ML lifecycle—from ETL and feature engineering to model training, LLM applications, multimodal RAG, MLOps, deployment, and monitoring. Skilled in Python, FastAPI, PostgreSQL (pgvector), LangChain, and cloud-ready AI systems. Currently completing an MBA in Artificial Intelligence & Machine Learning, combining strong technical expertise with business strategy.]

    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key,value)
    doc.save("Resume_1.docx")

if __name__=="__main__":
    resumeEdit()
    data ={
        '[template]':'I have 3 years of experience building python based applications'
    }

