from .starting import State  # or .starting if run as -m module
from .resume_builder import resume_evaluator  # adjust to actual filename

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

result = resume_evaluator(fake_state)
print("RESULT:")
print(result)