# cmd_test

A simple Python command-line application for testing basic arithmetic operations with unit tests.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [How to Add This README to the Repository](#how-to-add-this-readme-to-the-repository)

## Description

`cmd_test` is a lightweight Python script that defines functions for running sequential tests of command line tools.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/daniel-hancock33/cmd_test.git


# Key Components Present
```
Module		Purpose
core/		Orchestrates test loading, execution, and reporting
executors/	Contains all script execution logic (bash, nzsql, etc.)
utils/		Contains reusable utility functions (env validation, logging, etc.)
scripts/	Holds raw SQL or Bash scripts referenced in YAML tests
tests/		Holds YAML files that define your test cases
reports/	Output for HTML, JSON, and text reports
output/		Stores individual test logs
logs/		(Optional) Central location for execution logs (if used by your system)
main.py	CLI 	entry point (should be nz_test/main.py if setup.py uses package)
setup.py	Defines installable CLI (nztest) and dependencies
```

## [Usage](#usage)

### Run only sample and acme, with emojis
`python3 main.py --include-tests sample acme --emoji`

### Run all except acme, no emoji output (default)
`python3 main.py --exclude-tests acme`

### Run everything, with emoji output
`python3 main.py --emoji`
