import argparse
import os
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
    parser.add_argument("--test-dir", default="tests", help="Root directory containing test folders")
    parser.add_argument("--dry-run", action="store_true", help="Echo commands without running")
    parser.add_argument("--emoji", action="store_true", help="Enable emoji output")
    parser.add_argument("--include-tests", nargs="*", help="List of test subdirectories to include")
    parser.add_argument("--exclude-tests", nargs="*", help="List of test subdirectories to exclude")

    args = parser.parse_args()

    # Emojis are off by default unless --emoji is passed
    helpers.USE_EMOJIS = args.emoji

    selected_tags = set(t.strip() for t in args.tags.split(",") if t.strip())

    # Determine which test directories to run
    test_root = args.test_dir
    all_dirs = [
        d for d in os.listdir(test_root)
        if os.path.isdir(os.path.join(test_root, d))
    ]

    if args.include_tests:
        selected_dirs = [d for d in args.include_tests if d in all_dirs]
    else:
        selected_dirs = all_dirs

    if args.exclude_tests:
        selected_dirs = [d for d in selected_dirs if d not in args.exclude_tests]

    test_dirs = [os.path.join(test_root, d) for d in selected_dirs]

    # Load all tests from final list of directories
    all_tests = []
    for test_dir in test_dirs:
        all_tests.extend(load_tests(test_dir))

    if not all_tests:
        helpers.log_line("ERROR", "No test cases found", "Exiting.")
        exit(1)

    check_env_vars(all_tests)

    if selected_tags:
        all_tests = [t for t in all_tests if selected_tags & set(t.get("tags", []))]

    results, output_dir, run_id = run_tests(
        all_tests,
        dry_run=args.dry_run,
        label=args.label
    )

    write_report(results, label=args.label, run_id=run_id)
    generate_html_report(results, label=args.label, timestamp=run_id)
    print_summary(results, label=args.label, output_dir="reports", run_id=run_id)

if __name__ == "__main__":
    main()
