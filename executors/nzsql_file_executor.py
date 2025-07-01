# File: executors/nzsql_file_executor.py
# ---
# This module provides a function to run nzsql files using subprocess.
# It handles the execution of nzsql files, capturing their output and return status.

import subprocess
import os

def run_nzsql_file(database, sql_file, output_path=None):
    env = os.environ.copy()
    nzsql_cmd = [
        "nzsql",
        "-d", database,
        "-f", sql_file,
    ]

    try:
        result = subprocess.run(
            nzsql_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
            text=True
        )
        output = result.stdout.strip()

        # Write to output file if requested
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(output)

        success = result.returncode == 0
        return success, output
    except Exception as e:
        return False, f"Error executing nzsql script: {str(e)}"
