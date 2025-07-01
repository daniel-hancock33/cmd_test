# File: core/loader.py
# ---
# This module is responsible for loading test definitions from YAML files.
# It traverses the specified directory structure, reads YAML files,
# and extracts test cases into a list of dictionaries. Each test case
# includes the file path for reference, allowing for easy identification
# and debugging of tests. The loaded tests can then be used by the runner
# to execute the defined commands and validate their outcomes.
# It uses the PyYAML library to parse YAML files and extract test definitions.
# The tests are expected to be defined in a specific format within the YAML files,
# typically under a "tests" key, where each test case is a dictionary containing
# the necessary information such as command, executor type, and expected outcomes.
import os
import yaml

def load_tests(test_dir):
    all_tests = []
    for root, _, files in os.walk(test_dir):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                path = os.path.join(root, f)
                with open(path) as infile:
                    doc = yaml.safe_load(infile)
                    for test in doc.get("tests", []):
                        test["__file__"] = path  # Inject path info
                        all_tests.append(test)
    return all_tests

