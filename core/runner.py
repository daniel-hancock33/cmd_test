# File: core/runner.py
# ---
# This module contains the main logic for executing test cases.
# It imports various executor functions for running different types of commands,
# such as bash scripts, nzsql commands, and nzsql files.
# The run_test function is responsible for executing a single test case,
# managing the output directory structure, and handling the test execution logic.
# The run_tests function iterates over a list of test cases, executing each one
# and collecting the results. It also manages the output directory structure
# based on the run ID and label provided, ensuring that results are organized
# by test file for easier debugging and review.
# The results from each test execution are returned, allowing for easy reporting
# and analysis after all tests have been executed.
# The output directory structure is designed to keep results organized by run,
# making it easier to locate and review test outputs later.
import os
from datetime import datetime
from utils.helpers import log_line
from executors.bash_executor import run_bash
from executors.nzsql_executor import run_nzsql
from executors.nz_executor import run_nz
from executors.nzsql_file_executor import run_nzsql_file

# Maps each executor type to the appropriate function
# Type of process to run, bash script, nzsql command, or nzsql file
# The executors are imported from their respective modules
# This allows for easy extension in the future if new executors are added
# Each executor function should return a tuple (status, output)
# where status is a boolean indicating success/failure,
# and output is the command output or error message.
# The executors are expected to handle their own logging and output management.
EXECUTOR_MAP = {
    'bash': run_bash,
    'nzsql': run_nzsql,
    'nz': run_nz,
    'nzsql_file': run_nzsql_file
}

# This function runs a single test case, managing the output directory structure
# and handling the execution logic based on the executor type specified in the test definition.
# It captures the output and status of the test execution, writing results to a log file.
# The function also handles dry runs, skips, and errors gracefully,
# ensuring that the test results are well-structured and easy to analyze later.
# It returns a dictionary containing the test name, executor type, command,
# status, output, duration, and the path to the output file.
# The output directory is created based on the test file's location,
# allowing for organized storage of test results.
# The function also logs the start, success, failure, and error states of the test execution
# to provide clear feedback on the test run process.
# The output file is named based on the test name, ensuring uniqueness and clarity.
# The function is designed to be reusable and modular, allowing for easy integration
# into a larger test framework or suite.
# It is expected to be called by the run_tests function, which manages multiple test cases.
# The function also supports skipping tests based on configuration,
# allowing for flexible test execution based on user-defined conditions.
def run_test(test, base_output_dir, dry_run=False):
    #name = test.get('name', 'Unnamed Test')

    short_name = test.get('name', 'Unnamed Test')
    rel_path = os.path.relpath(os.path.dirname(test.get('__file__', 'misc')), 'tests')
    name = f"{rel_path}/{short_name}"

    executor = test.get('executor', 'bash')
    command = test.get('command', '')
    test_file = test.get('__file__', '')
    test_dir = os.path.dirname(test_file)
    #test_output_dir = os.path.join(base_output_dir, test_dir)
    test_output_dir = os.path.join(base_output_dir, rel_path)
    os.makedirs(test_output_dir, exist_ok=True)

    #safe_name = name.replace(" ", "_").lower()
    safe_name = short_name.replace(" ", "_").lower()
    out_path = os.path.join(test_output_dir, f"{safe_name}.log")

    result = {
        'name': name,
        'executor': executor,
        'command': command,
        'status': 'UNKNOWN',
        'output': '',
        'duration_sec': 0,
        'output_file': out_path,
    }

    if test.get('skip', False):
        result['status'] = 'SKIPPED'
        result['output'] = 'Test skipped by configuration.'
        log_line("SKIP", "Skipping Test", f"{name} (marked skip: true)")
        return result

    if dry_run:
        result['status'] = 'DRY_RUN'
        result['output'] = f"[DRY RUN] Would run: {executor} -> {command}"
        with open(out_path, "w") as f:
            #f.write(result['output'])
            f.write(result['output'].rstrip() + "\n")
        log_line("RUN", "Dry Run", name)
        return result

    try:
        log_line("START", "Starting Test", name)
        start = datetime.now()

        if executor == "nzsql_file":
            db = test.get("database")
            sql_file = os.path.join(test_dir, test["sql_file"])
            status, output = run_nzsql_file(db, sql_file, output_path=out_path)
        elif executor == "bash":
            full_command = os.path.join(test_dir, command)
            status, output = run_bash(full_command)
        else:
            func = EXECUTOR_MAP.get(executor)
            if func:
                status, output = func(command)
            else:
                status, output = False, f"Unknown executor: {executor}"

        duration = (datetime.now() - start).total_seconds()
        result['status'] = 'PASS' if status else 'FAIL'
        result['output'] = output
        result['duration_sec'] = duration

        #with open(out_path, "w") as f:
        #    f.write(output)
        with open(out_path, "w") as f:
            f.write(output.rstrip() + "\n")


        log_line("RUN", "Running Test", name)
        log_line("SUCCESS" if result['status'] == "PASS" else "FAIL", "Status", f"{result['status']:<6} ({duration:.3f}s)")
        log_line("INFO", "Output File", out_path)

    except Exception as e:
        result['status'] = 'ERROR'
        result['output'] = str(e)
        with open(out_path, "w") as f:
            #f.write(str(e))
            f.write(str(e).rstrip() + "\n")

        log_line("ERROR", "Error", str(e))

    return result

# This function runs a list of tests, executing each one in sequence.
# It honors the `depends_on_previous` flag, skipping tests if the previous one failed
# and logging the results. The results are returned along with the output directory
# and run ID for further processing or reporting.
def run_tests(tests, dry_run=False, output_dir_base="output", label="system"):
    """
    Executes all test cases provided in the list, honoring `depends_on_previous`.

    Args:
        tests (list): List of test dictionaries.
        dry_run (bool): If True, commands are not executed.
        output_dir_base (str): Base output folder for logs.
        label (str): Custom label used in output folder naming.

    Returns:
        tuple: (results list, full output directory path, run_id timestamp string)
    """
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output_dir = os.path.join(output_dir_base, f"{run_id}_{label}")
    results = []

    for idx, test in enumerate(tests):
        # If depends_on_previous is set and previous test failed, mark this one as skipped
        if test.get("depends_on_previous") and idx > 0:
            prev_status = results[-1].get("status")
            if prev_status != "PASS":
                test["skip"] = True
                log_line("SKIP", "Skipped due to failure in previous test", test["name"])
        result = run_test(test, base_output_dir, dry_run=dry_run)
        results.append(result)

    return results, base_output_dir, run_id
