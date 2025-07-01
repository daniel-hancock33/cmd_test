# File: core/summary.py
# ---
# This module contains functions to print a summary of test results.
# It aggregates the results by status (PASS, FAIL, ERROR, DRY_RUN,
# SKIPPED and prints a formatted summary to the console.
# It also generates a summary file in the output directory.
# The summary includes the count of each status and the total number of tests run.
# Additionally, it lists the generated report files and their locations.
from utils.helpers import log_line, USE_EMOJIS

# Function to print a summary of test results
# It aggregates results by status and prints a formatted summary.
# It also generates a summary file in the output directory.
# The summary includes counts of each status and the total number of tests run.
# Additionally, it lists the generated report files and their locations.
def print_summary(results, label, output_dir, run_id):
    summary = {"PASS": 0, "FAIL": 0, "ERROR": 0, "DRY_RUN": 0, "SKIPPED": 0}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1

    print()
    log_line("", "Test Summary")
    for status in ["PASS", "FAIL", "ERROR", "DRY_RUN", "SKIPPED"]:
        log_line("", f"{status:<10}", summary.get(status, 0), indent=2)
    log_line("", f"{'TOTAL':<10}", len(results), indent=2)

    summary_path = f"{output_dir}/{run_id}_{label}_summary.txt"
    with open(summary_path, "w") as f:
        f.write("Test Summary\n")
        for status in ["PASS", "FAIL", "ERROR", "DRY_RUN", "SKIPPED"]:
            f.write(f"{status:<8}: {summary.get(status, 0)}\n")
        f.write(f"{'TOTAL':<8}: {len(results)}\n")

    print()
    if USE_EMOJIS:
        log_line("🗂️", "Generated Files")
        log_line("📄", "JSON Report", f"reports/{run_id}_{label}.json")
        log_line("📊", "HTML Report", f"reports/{run_id}_{label}.html")
        log_line("📄", "Summary (txt)", f"reports/{run_id}_{label}_summary.txt")
        log_line("📂", "Output Logs", f"{output_dir}/")
    else:
        log_line("", "Generated Files")
        log_line("", "JSON Report", f"reports/{run_id}_{label}.json", indent=2)
        log_line("", "HTML Report", f"reports/{run_id}_{label}.html", indent=2)
        log_line("", "Summary (txt)", f"reports/{run_id}_{label}_summary.txt", indent=2)
        log_line("", "Output Logs", f"{output_dir}/", indent=2)
