# File: utils/env_check.py
# ---
# This module checks for the presence of required environment variables.
import os
from utils.helpers import log_line

REQUIRED_ENV_VARS = ["NZ_HOST", "NZ_USER", "NZ_PASSWORD"]

def check_env_vars(tests=None):
    missing = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
    if missing:
        for var in missing:
            log_line("ERROR", "Missing ENV", var)
        print("Environment check failed. Exiting.")
        exit(1)
    else:
        log_line("INFO", "All required environment variables are set")
