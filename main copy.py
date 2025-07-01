# File: main.py
# ---
# This is the main entry point for the test suite.
# It handles command-line arguments, loads test definitions, runs the tests,
# and generates reports.
import argparse
from core.loader import load_tests
from core.runner import run_tests
from core.report import write_report
from core.summary import print_summary
from utils.env_check import check_env_vars
from utils import helpers
from utils.report_utils import generate_html_report


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", help="Comma-separated tag filter", default="")
    parser.add_argument("--label", help="Label for this run (e.g., 'nextgen')", default="system")
    parser.add_argument("--test-dir", default="tests", help="Path to test YAMLs")
    parser.add_argument("--dry-run", action="store_true", help="Echo commands without running")
    parser.add_argument("--no-emoji", action="store_true", help="Disable emoji output")
    parser.add_argument("--include-tests", nargs="*", help="List of test subdirectories to include")

    args = parser.parse_args()

    # Enable/disable emojis based on CLI flag
    helpers.USE_EMOJIS = not args.no_emoji

    # Parse tags from input to filter tests
    selected_tags = set(t.strip() for t in args.tags.split(",") if t.strip())
    
    # Load test definitions from YAML files
    all_tests = load_tests(args.test_dir)

    if not all_tests:
        helpers.log_line("ERROR", "No test cases found", "Exiting.")
        exit(1)

    # Check for required environment variables based on the test definitions
    check_env_vars(all_tests)

    # Filter tests by tag
    if selected_tags:
        all_tests = [t for t in all_tests if selected_tags & set(t.get("tags", []))]

    # Run the tests and capture results
    results, output_dir, run_id = run_tests(
        all_tests,
        dry_run=args.dry_run,
        label=args.label
    )
    
    # Write reports and summaries
    write_report(results, label=args.label, run_id=run_id)
    generate_html_report(results, label=args.label, timestamp=run_id)
    print_summary(results, label=args.label, output_dir="reports", run_id=run_id)

if __name__ == "__main__":
    main()
