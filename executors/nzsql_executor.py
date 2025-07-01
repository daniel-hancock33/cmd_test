# File: executors/nzsql_executor.py
# ---
# This module provides a function to run nzsql commands using subprocess.
# It handles the execution of nzsql commands, capturing their output and return status.
import subprocess
import os

def run_nzsql(command):
    env = os.environ.copy()
    nzsql_cmd = [
        "nzsql",
        "-d", env.get("NZ_DATABASE", ""),
        "-c", command
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
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, f"Error executing nzsql: {str(e)}"
