# File: executors/nz_executor.py
# ---
# This module provides a function to run nz commands using subprocess.
# It handles the execution of nz commands, capturing their output and return status.
import subprocess
import os

def run_nz(command):
    env = os.environ.copy()
    try:
        result = subprocess.run(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
            text=True
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, f"Error running nz command: {str(e)}"
