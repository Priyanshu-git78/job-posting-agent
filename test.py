
from config import get_llm
from pydantic import BaseModel , Field



llm = get_llm()

highlight_phrases = [
        "2+ years",
        "Machine Learning",
        "ETL",
        "FastAPI",
        "PostgreSQL (pgvector)",
        "MBA in Artificial Intelligence & Machine Learning",
    ]
bio ="""AI/ML Engineer with 3+ years of experience designing, orchestrating, and deploying enterprise-grade agentic AI systems. Skilled in building multi-agent workflows with LangChain and LangGraph — combining reasoning, planning, and tool-calling with enterprise application and API integration. Experienced building production RAG pipelines with hybrid retrieval (dense + BM25) across vector databases including pgvector, Pinecone, and Azure AI Search, and deploying containerized AI services with Docker and Kubernetes on AWS, Azure, and GCP. Background spans full-lifecycle delivery — from ETL and evaluation/observability (MLflow, LangSmith, DeepEval) to production monitoring — with an MBA in AI & ML adding a business-outcomes lens to technical delivery."""
prompt = f"""You are helping an HR reviewer quickly scan a candidate's bio by highlighting the most important information.

Extract every phrase from the bio below that an HR reviewer should see at a glance, including:
- Job titles, years of experience, and career progression
- Technical skills, tools, and certifications
- Quantifiable achievements (e.g., "increased revenue by 30%")
- Education and degrees
- Notable companies or projects
- Any red flags or gaps worth noting (e.g., unexplained employment gaps)

Rules:
- Only extract phrases that appear verbatim in the bio — do not paraphrase or invent text.
- Do not include generic filler (e.g., "hardworking team player") unless tied to a specific, verifiable claim.
- Return ONLY the phrases, no commentary or explanation.

Output format — return a JSON list matching this exact structure:
{highlight_phrases}

Bio to analyze:
\"\"\"
{bio}
\"\"\"
"""
llm_structure = llm.with_structured_output(highlighting)


response = llm_structure.invoke(prompt)
print(response)