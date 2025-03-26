"""
function_registry.py

Stores all the automation functions that we want our LLM-based system to call.
Includes metadata for each function so we can do RAG-based retrieval.
"""

import os
import webbrowser
import psutil
import subprocess

def open_calculator():
    """
    Opens the calculator application.

     On Windows, 'calc' works.
    """
    # On Windows:
    os.system("calc")
    

def open_chrome():
    """
    Opens Google Chrome in a browser window.
    """
    webbrowser.open("https://www.google.com")


def check_ram_usage():
    """
    Returns the current system RAM usage as a percentage.
    """
    memory_info = psutil.virtual_memory()
    return f"RAM Usage: {memory_info.percent}%"

def run_shell_command(command: str):
    """
    Runs a shell command and returns its output.
    """
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"

# -----------------------------------------------------
#  METADATA for each function.
#  We'll use these descriptions to generate embeddings
#  so we can figure out the best match for user queries.
# -----------------------------------------------------
FUNCTIONS_METADATA = [
    {
        "name": "open_calculator",
        "description": "Open the calculator application on the system."
    },
    {
        "name": "open_chrome",
        "description": "Open Google Chrome to the home page."
    },
    {
        "name": "check_ram_usage",
        "description": "Check the system RAM usage and return it as a percentage."
    },
    {
        "name": "run_shell_command",
        "description": "Run a provided shell command and return its output."
    },
]
