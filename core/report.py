# File: core/report.py
# ---
# This module contains functions for writing test results to a report file.
# It handles the creation of the output directory, formatting the results,
# and saving the results in JSON format. The report can be labeled and organized
# by run ID, allowing for easy tracking of test runs over time.
# The report is saved in a specified output directory, and the directory is created if it does not exist.
# The report file is named using the run ID and label, ensuring that each report is unique
# and can be easily identified later. The results are saved in a JSON format for easy readability
# and potential further processing or analysis.
import os
import json
from datetime import datetime


def write_report(results, label="system", output_dir="reports", run_id=None):
    os.makedirs(output_dir, exist_ok=True)
    if not run_id:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{output_dir}/{run_id}_{label}.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
