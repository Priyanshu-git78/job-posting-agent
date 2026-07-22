# job-posting-agent

LangGraph agent that extracts structured job & company details from a link or pasted posting, with resume-fit analysis planned — powered by a local LLM.

## Overview

`job-posting-agent` accepts **either**:
- a **job posting URL**, or
- **raw pasted job posting text**

and turns it into structured data: company name, role title, required skills, and responsibilities — via an LLM running locally (no external API keys required).

An LLM-free routing step inspects the input and decides whether it needs to be fetched from the web first, or is already usable content — then a structured-output LLM call extracts the fields into a typed schema.

```
              ┌──────────────┐
  user_input ─┤  route_start │
              └──────┬───────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
   looks like a URL          already text
        │                           │
        ▼                           │
 ┌─────────────┐                    │
 │  search_url │  (fetch page)      │
 └──────┬──────┘                    │
        │                           │
        └─────────────┬─────────────┘
                       ▼
        ┌───────────────────────────┐
        │ company_details_extractor │
        │   (LLM structured output) │
        └─────────────┬─────────────┘
                       ▼
                     END
```

## Features

- 🔀 **Smart routing** — automatically detects whether the input is a link or raw text and takes the right path through the graph
- 🌐 **Web fetching** — pulls page content via `WebBaseLoader` when given a URL
- 🧠 **Structured extraction** — uses `with_structured_output` to reliably parse company name, job title, required skills, and responsibilities into a typed Pydantic model
- 💾 **Stateful sessions** — powered by LangGraph's checkpointer, so each run/thread keeps its own state
- 🖥️ **Streamlit UI** — simple chat-style interface for pasting a link or job description
- 🏠 **Runs locally** — designed to work against a local OpenAI-compatible LLM server (e.g. Qwen3-4B via vLLM), no cloud API key needed

## Roadmap

- [ ] Resume-fit scoring — compare a candidate's resume against the extracted job requirements (`my_resume_rank_against_it`)
- [ ] Gap analysis — surface concrete shortcomings vs. the role's requirements (`my_shortcoming`)
- [ ] Headless-browser fetching (Playwright) for JS-rendered job boards (e.g. Indeed) where static HTML fetching returns incomplete content
- [ ] Support for additional job board formats and structured (JSON-LD) extraction where available

## Tech stack

| Layer | Tool |
|---|---|
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM interface | [LangChain](https://github.com/langchain-ai/langchain) (`init_chat_model`) |
| Local LLM | Qwen3-4B served via an OpenAI-compatible endpoint |
| Web fetching | `langchain_community.document_loaders.WebBaseLoader` |
| UI | [Streamlit](https://streamlit.io/) |
| Schema validation | [Pydantic](https://docs.pydantic.dev/) |

## Getting started

### Prerequisites

- Python 3.11+
- A running OpenAI-compatible LLM server (e.g. [vLLM](https://github.com/vllm-project/vllm) serving Qwen3-4B) reachable at a local endpoint

### Installation

```bash
git clone https://github.com/<your-username>/job-posting-agent.git
cd job-posting-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Set the environment variable required by `WebBaseLoader` to identify outbound requests:

```bash
export USER_AGENT="job-posting-agent/1.0"
```

Update the LLM connection settings in the code to match your local server:

```python
llm = init_chat_model(
    model="Qwen/Qwen3-4B",
    openai_api_base="http://localhost:8005/v1",
    openai_api_key="<your-key>",
    model_provider="openai",
    temperature=0.0,
)
```

### Running the CLI script

```bash
python link_to_register.py
```

### Running the Streamlit app

```bash
streamlit run app.py
```

Then paste a job posting link or the full text of a posting into the chat box.

## Project structure

```
.
├── link_to_register.py   # LangGraph definition: state, nodes, routing, graph
├── app.py                 # Streamlit front end
├── requirements.txt
└── README.md
```

## How it works

1. **`route_start`** inspects the raw input and decides the next node:
   - starts with `http://` or `https://` → routes to `search`
   - otherwise → routes directly to `company_details_extractor`
2. **`search_url`** fetches the page via `WebBaseLoader` and stores the extracted text in `page_content`
3. **`company_details_extractor`** sends the available content (fetched page or raw pasted text) to the LLM with a structured output schema (`companydetails`), returning:
   - `company_name`
   - `requirement_title`
   - `requirement_skill`
   - `requirement_responsibilities`

## Known limitations

- Some job boards (e.g. Indeed) render posting content client-side via JavaScript. `WebBaseLoader` performs a plain HTTP fetch and will not execute JS, so it may return the site's HTML shell rather than the actual job content for such pages. A headless-browser loader (Playwright) is planned to address this.
- Extraction quality depends on the local LLM's capability — smaller models may occasionally produce incomplete or imprecise field values.

## License

MIT (or update to your preferred license)

## Contributing

Issues and pull requests are welcome.