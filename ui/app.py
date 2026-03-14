from flask import Flask, request, render_template, redirect, url_for
import os
import json

from core.orchestrator import run_analysis
from utils.folder_manager import normalize_company_name
from config import COMPANY_DATA_DIR
from utils.logger import log

app = Flask(__name__)


def collect_results(company_path):
    """Traverse the company output folder and load all JSON files."""
    results = {}
    for root, dirs, files in os.walk(company_path):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, company_path)
            try:
                with open(full, "r") as f:
                    results[rel] = json.load(f)
            except Exception as e:
                results[rel] = f"<unable to load: {e}>"
    return results


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("company")
    if not user_input:
        return redirect(url_for("index"))

    try:
        company_path = run_analysis(user_input)
    except Exception as e:
        log(f"Analysis exception: {e}", level="ERROR")
        return render_template("results.html", error=str(e))

    if not company_path:
        return render_template("results.html", error="Entity resolution failed or no data generated.")

    results = collect_results(company_path)
    # pass the normalized name so we can show path if needed
    return render_template("results.html", company=user_input, data=results)


if __name__ == "__main__":
    # allow port override via environment variable UI_PORT
    try:
        port = int(os.getenv("UI_PORT", 5000))
    except ValueError:
        port = 5000
    app.run(debug=True, port=port)
