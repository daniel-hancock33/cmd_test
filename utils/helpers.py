# File: utils/helpers.py
# ---
# This module provides utility functions for logging and formatting output.
from datetime import datetime

USE_EMOJIS = True  # Default to True

EMOJI_PREFIXES = {
    "START": "🚀",
    "RUN": "▶️",
    "SUCCESS": "✅",
    "FAIL": "❌",
    "SKIP": "⏭️",
    "ERROR": "💥",
    "INFO": "📄",
    "SUMMARY": "🔍",
    "FILES": "🗂️",
    "REPORT": "📊",
}

LABEL_PREFIXES = {
    "START": "[START    ]",
    "RUN": "[RUN      ]",
    "SUCCESS": "[SUCCESS  ]",
    "FAIL": "[FAIL     ]",
    "SKIP": "[SKIPPED  ]",
    "ERROR": "[ERROR    ]",
    "INFO": "[INFO     ]",
    "SUMMARY": "[SUMMARY  ]",
    "FILES": "[FILES    ]",
    "REPORT": "[REPORT   ]",
}

def log_line(prefix_key, label="", value="", indent=0):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    indent_space = " " * indent
    prefix = EMOJI_PREFIXES.get(prefix_key, "") if USE_EMOJIS else LABEL_PREFIXES.get(prefix_key, "")
    print(f"{ts} {indent_space}{prefix} {label:<15} : {value}")

# def log_line(prefix_key, label="", value="", indent=0):
#     ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     indent_space = " " * indent
#     prefix = EMOJI_PREFIXES.get(prefix_key, "") if USE_EMOJIS else LABEL_PREFIXES.get(prefix_key, "")
#     colon = ":" if value else ""
#     print(f"{ts} {indent_space}{prefix} {label:<12}{colon} {value}")
