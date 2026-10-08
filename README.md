# LegalEase

LegalEase is an AI-powered legal and policy simplifier for an NLP project submission. It accepts PDF, TXT, or pasted document text, performs traditional NLP preprocessing, chunks long documents, and uses an LLM API to produce a plain-language report.

The app focuses on the question:

> What does this document mean for me?

## Features

- Streamlit web interface
- PDF, TXT, and pasted-text input
- Page-aware PDF extraction with `pypdf`
- Text cleaning, sentence splitting, tokenization, and document statistics
- Configurable chunking with overlap
- Prompt files separated from application code
- LLM client abstraction with OpenAI-compatible API support
- Offline demo mode when no API key is configured
- Structured report sections:
  - Short summary
  - What this means for me
  - Important obligations
  - User rights
  - Deadlines
  - Fees and penalties
  - Potential risks
  - Questions to consider

## Project Structure

```text
Legalpolicy/
  app.py
  requirements.txt
  .env.example
  config/
    config.yaml
  prompts/
    chunk_analysis_prompt.txt
    final_synthesis_prompt.txt
  legalease/
    analysis.py
    chunker.py
    config.py
    document_loader.py
    llm_client.py
    models.py
    preprocessing.py
    prompt_manager.py
    response_parser.py
  tests/
    test_chunker.py
    test_config.py
    test_preprocessing.py
    test_response_parser.py
```

## Setup

1. Create a virtual environment.

```bash
python -m venv .venv
```

2. Activate it.

```bash
.venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create your environment file.

```bash
copy .env.example .env
```

5. Add your API key to `.env`.

```text
LLM_API_KEY=your_api_key_here
```

## Run

```bash
streamlit run app.py
```

## Testing

```bash
pytest
```

## Notes

LegalEase is for informational explanation only. It does not provide legal advice and should not be used as a replacement for a qualified lawyer.
