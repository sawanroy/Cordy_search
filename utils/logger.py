# utils/logger.py

import datetime
import threading
import time

current_stage = None


def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def set_stage(stage_name: str):
    global current_stage
    current_stage = stage_name
    log(f"STAGE: {stage_name}", level="STAGE")


def heartbeat_monitor(timeout_seconds=300):
    """
    If a stage runs too long, log freeze warning.
    """
    start_time = time.time()

    while True:
        time.sleep(10)
        elapsed = time.time() - start_time

        if current_stage:
            log(f"Heartbeat: Stage '{current_stage}' running for {int(elapsed)} sec", level="HEARTBEAT")

        if elapsed > timeout_seconds:
            log(f"WARNING: Stage '{current_stage}' exceeding expected time!", level="WARNING")
            break