# Competitive Intelligence Agent

This repository provides a CLI/HTTP interface for scraping e-commerce marketplaces and performing revenue analysis for a given company.

## Getting started

1. Create a Python environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ensure Ollama is installed and accessible (`ollama serve`). The project will start it if necessary.

## Running

### Command-line

```bash
python main.py
```

Enter a company name, website or CIN when prompted. The results will be written to `company_data/<normalized_name>/`.

### Web UI

Start a simple Flask UI:

```bash
python main.py --ui
```

Open your browser to `http://localhost:5000/`, type in a company name, and submit. Results are shown on the page.


## Code structure

- `core/orchestrator.py` – pipeline coordinator
- `modules/` – logic for entity resolution, crawling, revenue
- `utils/` – helpers for scraping, logging, progress, folders
- `ui/` – Flask application and templates

Enjoy exploring!"