# File: executors/bash_executor.py
# ---
# This module provides a function to run bash commands using subprocess.
import subprocess

def run_bash(command):
    try:
        result = subprocess.run(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            text=True
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, f"Error running bash command: {str(e)}"
