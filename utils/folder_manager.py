# utils/folder_manager.py

import os
import json
from config import COMPANY_DATA_DIR
from utils.logger import log

def normalize_company_name(name: str) -> str:
    return name.strip().replace(" ", "_").replace("/", "_")

def create_company_structure(company_name: str):
    normalized = normalize_company_name(company_name)
    base_path = os.path.join(COMPANY_DATA_DIR, normalized)

    subfolders = [
        "marketplace",
        "products",
        "revenue",
        "analysis",
        "raw_scrapes",
        "logs"
    ]

    os.makedirs(base_path, exist_ok=True)

    for folder in subfolders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    metadata_path = os.path.join(base_path, "metadata.json")
    if not os.path.exists(metadata_path):
        with open(metadata_path, "w") as f:
            json.dump({"company_name": company_name}, f, indent=4)

    log(f"Company folder prepared at {base_path}")
    return base_path
