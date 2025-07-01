# File: utils/report_utils.py
# ---
# This module contains functions for generating HTML reports from test results.
import os
from jinja2 import Environment, FileSystemLoader

def generate_html_report(results, label="system", timestamp=""):
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), "templates"))
    )
    template = env.get_template("report_template.html")

    output_html = template.render(
        results=results,
        label=label,
        timestamp=timestamp
    )

    output_path = os.path.join(reports_dir, f"{timestamp}_{label}.html")
    with open(output_path, "w") as f:
        f.write(output_html)
