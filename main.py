# main.py

import os

from core.orchestrator import run_analysis
from utils.logger import log

def main():
    print("=================================")
    print("Competitive Intelligence Agent")
    print("=================================\n")

    import argparse

    parser = argparse.ArgumentParser(description="Competitive Intelligence Agent")
    parser.add_argument("--ui", action="store_true", help="Start web UI instead of CLI")
    parser.add_argument("--port", type=int, default=int(os.getenv("UI_PORT", 5000)),
                        help="Port for the web UI (default via UI_PORT env or 5000)")
    args = parser.parse_args()

    if args.ui:
        # run the flask app
        from ui.app import app
        app.run(debug=True, port=args.port)
        return

    user_input = input("Enter Company Name / Website / CIN: ").strip()

    if not user_input:
        print("Invalid input.")
        return

    try:
        run_analysis(user_input)
        print("\nAnalysis completed successfully.")
    except Exception as e:
        log(str(e), level="ERROR")

if __name__ == "__main__":
    main()
