# core/orchestrator.py

import os
import json

from modules.entity_resolver import resolve_entity
from modules.legal_identity import extract_legal_identity
from modules.marketplace_finder import find_marketplaces
from modules.deep_crawl_engine import DeepCrawlEngine
from modules.revenue.revenue_engine import RevenueEngine

from utils.folder_manager import create_company_structure
from utils.logger import log
from utils.ollama_manager import ensure_ollama_ready
from utils.progress import ProgressBar



def run_analysis(user_input: str):

    log("Starting analysis pipeline...")

    tasks = [
        "Ollama Check",
        "Entity Resolution",
        "Folder Creation",
        "Legal Identity",
        "Marketplace Discovery",
        "Deep Multi-Channel Crawl",
        "Revenue Analysis"
    ]

    progress = ProgressBar(total_tasks=len(tasks))

    # Task 1
    progress.set_stage("Ollama Check")
    ensure_ollama_ready()
    progress.update()

    # Task 2
    progress.set_stage("Entity Resolution")
    entity_data = resolve_entity(user_input)
    progress.update()

    if not entity_data.get("top_result"):
        log("Entity resolution failed.", level="ERROR")
        return None

    company_name = entity_data["top_result"].get("title", "Unknown_Company")

    # Task 3
    progress.set_stage("Folder Creation")
    company_path = create_company_structure(company_name)

    entity_file = os.path.join(company_path, "entity_resolution.json")
    with open(entity_file, "w") as f:
        json.dump(entity_data, f, indent=4)

    progress.update()

    # Task 4
    progress.set_stage("Legal Identity")
    extract_legal_identity(entity_data, company_path)
    progress.update()

    # Task 5
    progress.set_stage("Marketplace Discovery")
    find_marketplaces(company_name, company_path)
    progress.update()

    # Task 6
    # Deep Multi-Channel Crawl
    progress.set_stage("Deep Multi-Channel Crawl")

    engine = DeepCrawlEngine()
    engine.run(company_name, company_path)

    progress.update()

    # Revenue Stage
    progress.set_stage("Revenue Analysis")

    revenue_engine = RevenueEngine(company_path)
    revenue_engine.run()

    progress.update()

    progress.finish()

    # return the company directory so callers (e.g. a UI) can inspect results
    return company_path
