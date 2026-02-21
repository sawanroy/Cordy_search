# main.py

from core.orchestrator import run_analysis
from utils.logger import log

def main():
    print("=================================")
    print("Competitive Intelligence Agent")
    print("=================================\n")

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
