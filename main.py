"""
main.py

This is our FastAPI entry point. It exposes a /execute endpoint
to receive user prompts, retrieve the best function, (optionally)
generate a code snippet, and then run the function. We also log everything.
"""

import uvicorn
from fastapi import FastAPI, Body
import logging
import os
from vector_store import FunctionVectorStore
from code_generator import generate_code_snippet
import function_registry  # This is where our automation funcs live
from dotenv import load_dotenv

load_dotenv()  
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "app.log")

# Creating logs
os.makedirs(LOG_FOLDER, exist_ok=True)

# Set up basic logging config
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Initialize FastAPI
app = FastAPI(title="LLM + RAG Function Execution API")

# Initialize our vector store for RAG-based function retrieval
store = FunctionVectorStore()

@app.post("/execute")
def execute_function(prompt: str = Body(..., embed=True)):
    """
    Accepts a user prompt, finds the best matching function,
    (optionally) calls the LLM to generate a code snippet, 
    executes the function, logs everything, and returns a response.
    """
    try:
        # 1) RAG retrieval: find best matching function for the user's query
        best_match = store.search(prompt, top_k=1)
        function_name = best_match["name"]

        # 2) (Optional) Generate code snippet from LLM
        #    I'm letting the LLM produce a Python snippet that calls the function.
        snippet = generate_code_snippet(function_name)

        # 3) Actually call the function. 
        #    We have a direct handle to it in function_registry:
        func = getattr(function_registry, function_name, None)
        if not func:
            raise ValueError(f"Function '{function_name}' not found in registry.")

        # Some functions might return a string or None, so let's store any result
        result = func()  # If function returns anything, we store it
        if not result:
            result = "Function executed successfully."

        # 4) Logging for debugging / bonus
        logging.info(f"User Prompt: '{prompt}' | Matched Function: '{function_name}'")

        return {
            "prompt": prompt,
            "matched_function": function_name,
            "execution_result": result,
            "generated_code_snippet": snippet  # show user the code snippet
        }

    except Exception as e:
        logging.error(f"Error while executing function: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Run our FastAPI app. 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
