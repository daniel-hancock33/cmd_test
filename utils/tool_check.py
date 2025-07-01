# File: utils/tool_check.py
# ---
# This module checks for the presence of required tools in the system.
# It verifies that essential command-line tools are available for the test suite to function correctly.
# If any required tool is missing, it raises an EnvironmentError with a descriptive message.
import shutil
from utils.helpers import log_line

def check_nz_tools():
    required_tools = ["nzsql"]
    for tool in required_tools:
        if not shutil.which(tool):
            log_line("❌", "Missing Tool", tool)
            raise EnvironmentError(f"Required tool not found: {tool}")
        else:
            log_line("🔍", "Tool Check", f"{tool} found")
