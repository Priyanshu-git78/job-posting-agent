
from config import get_llm


llm = get_llm()

fake_state: State = {
    "user_input": "",
    "link": "",
    "page_content": "",
    "company_name": "Acme Corp",
    "requirement_title": "Backend Engineer",
    "requirement_skill": "Python, FastAPI, PostgreSQL",
    "requirement_responsibilities": "Build and maintain REST APIs, optimize database queries",
    "my_resume_rank_against_it": "",
    "my_shortcoming": "",
}

highlight_phrases = [
        "2+ years",
        "Machine Learning",
        "ETL",
        "FastAPI",
        "PostgreSQL (pgvector)",
        "MBA in Artificial Intelligence & Machine Learning",
    ]
bio ="""AI/ML Engineer with 3+ years of experience designing, orchestrating, and deploying enterprise-grade agentic AI systems. Skilled in building multi-agent workflows with LangChain and LangGraph — combining reasoning, planning, and tool-calling with enterprise application and API integration. Experienced building production RAG pipelines with hybrid retrieval (dense + BM25) across vector databases including pgvector, Pinecone, and Azure AI Search, and deploying containerized AI services with Docker and Kubernetes on AWS, Azure, and GCP. Background spans full-lifecycle delivery — from ETL and evaluation/observability (MLflow, LangSmith, DeepEval) to production monitoring — with an MBA in AI & ML adding a business-outcomes lens to technical delivery."""
response =llm.invoke(f"you need to get all the text which will be essential to highlighiting for the hr to review {bio} in this format {highlight_phrases}")
print(response)