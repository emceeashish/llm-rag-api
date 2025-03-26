"""
code_generator.py

Contains logic to call the Together.ai chat endpoint 
to generate dynamic Python code that calls our matched function.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env vars if present
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_code_snippet(function_name: str):
    """
    Calls the Together.ai chat endpoint, asking it to generate a code snippet 
    that imports and executes the matched function.
    
    If you prefer not to do dynamic code generation, you can skip this step 
    and just call the function directly.
    """
    if not TOGETHER_API_KEY:
        return "Error: Missing Together.ai API key or .env is not set."

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Here's the conversation-like payload. 
    # I'm telling it: "Generate a short code snippet that calls function_name from function_registry."
    user_prompt = f"""
    Write a Python code snippet that imports the function '{function_name}' 
    from 'function_registry.py' and executes it in a main() function. 
    Please include error handling.
    """

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # or whichever model you prefer
        "messages": [
            {"role": "system", "content": "You are a Python coding assistant."},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 250,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # The actual generated code snippet
        generated_code = data["choices"][0]["message"]["content"]
        return generated_code.strip()
    except Exception as e:
        return f"Error generating code snippet: {e}"
