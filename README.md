# Resume Tailoring Agent

An AI-assisted resume tailoring workflow that turns a job-posting URL or pasted job description into a job analysis and a tailored resume. The application uses LangGraph to coordinate extraction, resume evaluation, content generation, document editing, and PDF export.

> This project is designed for a local, OpenAI-compatible LLM endpoint. No hosted OpenAI key is required when using a local server such as vLLM.

## What it does

1. Accepts a job-posting URL or pasted job description.
2. Fetches the page when the input is a URL.
3. Extracts the company, target title, skills, and responsibilities with structured LLM output.
4. Compares the role with the configured candidate resume.
5. Produces matching skills, relevant projects, gaps, a fit score, and an actionable summary.
6. Creates tailored resume content without inventing unsupported skills or experience.
7. Replaces placeholders in a DOCX template and exports the result as a PDF.

## Workflow

```text
Job URL or pasted description
             |
       route_start
        /          \
   URL: search       Text: extract details
        \          /
   company_details_extractor
             |
      resume_evaluator
             |
          summary
             |
         odx_editor
             |
        resumeEdit
             |
     resumes/resume.docx + resume.pdf
```

The workflow is compiled with an in-memory LangGraph checkpointer. Each app session receives a generated thread ID. A Mermaid diagram of the graph is also written to `technicals.png` whenever `graph_main()` runs.

## Requirements

- Python 3.11 or later
- A local OpenAI-compatible chat-completions endpoint, such as vLLM
- LibreOffice (`soffice`) on your `PATH` for DOCX-to-PDF conversion
- Internet access when submitting a job-posting URL

## Installation

This repository uses `uv` and includes a lockfile.

```bash
git clone <repository-url>
cd "Automation Scripts"
uv sync
```

Alternatively, create a virtual environment and install the project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

Create a `.env` file in the project root, or export the equivalent variables:

```dotenv
LLM_MODEL=Qwen/Qwen3-4B
VLLM_BASE_URL=http://localhost:8005/v1
VLLM_API_KEY=dummy-key
USER_AGENT=resume-tailoring-agent/1.0
```

`LLM_MODEL`, `VLLM_BASE_URL`, and `VLLM_API_KEY` configure the OpenAI-compatible LLM connection. The values above are the defaults used by `config.py`; change them to match your model server. `USER_AGENT` identifies requests made by the web loader and is recommended when processing URLs.

If using vLLM, start a server that exposes the OpenAI-compatible `/v1` API before launching the app.

## Run the app

```bash
uv run streamlit run streamlit.py
```

Or, in an activated virtual environment:

```bash
streamlit run streamlit.py
```

Enter either a full `http://`/`https://` job-posting URL or the full text of a job description. The Streamlit page displays the graph's node updates while the workflow runs.

## Candidate documents and outputs

The current implementation uses these project files:

| Purpose | Path |
| --- | --- |
| Source resume used for matching | `supported_documents/Priyanshu_Harsana_Resume.docx` |
| Resume template containing placeholders | `supported_documents/Priyanshu_Harsana_Template.docx` |
| Generated DOCX resume | `resumes/resume.docx` |
| Generated PDF resume | `resumes/resume.pdf` |
| Appended job-analysis data | `supported_documents/details.csv` |

To tailor the workflow to another candidate, replace the source resume and update the template while retaining its expected placeholders:

- `[bio]` for the professional summary
- `[skills]` for the categorized technical-skills section
- `[rag_experience]` for the RAG experience bullet

Generated output files are overwritten on each successful run. Job-analysis rows are appended to `supported_documents/details.csv`.

## Project layout

```text
.
├── config.py                 # LLM configuration loaded from environment variables
├── streamlit.py              # Streamlit chat interface
├── graph/
│   ├── graph.py              # LangGraph nodes and workflow wiring
│   ├── starting.py           # URL loading and job-detail extraction
│   └── resume_builder.py     # Resume analysis, template editing, and PDF export
├── supported_documents/      # Candidate source resume and DOCX template
├── resumes/                  # Generated resumes
├── pyproject.toml            # Project metadata and dependencies
└── uv.lock                   # Locked dependency versions
```

## Technology

- [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- [LangChain](https://python.langchain.com/) for model access and structured output
- [Streamlit](https://streamlit.io/) for the interface
- [Pydantic](https://docs.pydantic.dev/) for extraction schemas
- `python-docx` for DOCX editing
- LibreOffice headless mode for PDF conversion
- `WebBaseLoader` for static job-page retrieval

## Limitations

- URL fetching uses a static HTTP loader. Job boards that render descriptions client-side may return incomplete content.
- The candidate resume and template paths are currently hard-coded in `graph/resume_builder.py`.
- Extraction and tailoring quality depends on the model and the completeness of the job description and source resume.
- The generated documents are tailored suggestions and should be reviewed before use.

## Development notes

The `graph/test.py` and root `test.py` files are experimental LLM scripts rather than a complete automated test suite. Before relying on production output, validate the generated resume against the source material and target role.
