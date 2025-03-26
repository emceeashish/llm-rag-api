```markdown
# LLM + RAG Function Execution API

## Overview  
This API combines **Large Language Models (LLMs)** with **Retrieval-Augmented Generation (RAG)** to map natural language prompts (e.g., "Open calculator") to automation functions. It dynamically generates Python code, logs executions, and exposes endpoints via FastAPI.

---

## Table of Contents  
1. [Project Structure](#project-structure)  
2. [Key Components](#key-components)  
3. [Setup](#setup)  
4. [Usage](#usage)  
5. [Example Input/Output](#example-inputoutput)  
6. [Future Enhancements](#future-enhancements)

---

## Project Structure  
```
llm-rag-api/
├── .env                  # Stores Together.ai API key (not committed)
├── main.py               # FastAPI server and endpoint logic
├── function_registry.py  # Automation functions + metadata
├── embeddings.py         # Sentence-transformers embeddings
├── vector_store.py       # FAISS vector database
├── code_generator.py     # Together.ai (Mistral) code generation
├── requirements.txt      # Dependency list
└── logs/                 # Execution logs
```

---

## Key Components  

### 1. Function Registry  
- **File:** `function_registry.py`  
- **Functions:** `open_calculator()`, `open_chrome()`, `check_ram_usage()`, `run_shell_command()`  
- **Metadata:** Stored in `FUNCTIONS_METADATA` for RAG retrieval.  

### 2. Embeddings & Vector Store  
- **Embeddings Model:** `all-MiniLM-L6-v2` (sentence-transformers)  
- **Vector Store:** FAISS for fast similarity search.  

### 3. Dynamic Code Generation  
- **API:** Together.ai's Mistral model  
- **Output Example:**  
  ```python
  from function_registry import open_calculator
  open_calculator()
  ```

### 4. API Service  
- **Framework:** FastAPI  
- **Endpoint:** `/execute` (POST)  
- **Logging:** Saved to `logs/app.log`  

---

## Setup  

1. **Clone Repository**  
   ```bash
   git clone https://github.com/yourusername/llm-rag-api.git
   cd llm-rag-api
   ```

2. **Create Environment**  
   *Conda:*  
   ```bash
   conda create -n llm-rag python=3.10
   conda activate llm-rag
   ```  
   *Virtualenv:*  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   # Conda alternative:
   conda install -c conda-forge requests python-dotenv sentence-transformers faiss-cpu fastapi uvicorn psutil
   ```

4. **Configure API Key**  
   Create `.env` file:  
   ```ini
   TOGETHER_API_KEY=your_api_key_here
   ```

5. **Start Server**  
   ```bash
   uvicorn main:app --reload
   ```  
   Access docs: http://localhost:8000/docs  

---

## Usage  

1. **Send Request**  
   ```bash
   curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Check RAM usage"}'
   ```

2. **Response Format**  
   ```json
   {
     "matched_function": "check_ram_usage",
     "execution_result": "RAM usage: 45%",
     "generated_code_snippet": "from function_registry import check_ram_usage\ncheck_ram_usage()"
   }
   ```

3. **Verification**  
   - Physical results (e.g., calculator opens).  
   - Check logs: `tail -f logs/app.log`.  

---

## Example Input/Output  

**Input:**  
```json
{ "prompt": "Open calculator" }
```

**Output:**  
```json
{
  "matched_function": "open_calculator",
  "execution_result": "Function executed successfully",
  "generated_code_snippet": "from function_registry import open_calculator\nopen_calculator()"
}
```

**System Result:** Calculator app launches on Windows.  

---

## Future Enhancements  
- **Extended Functions:** Add file operations, email automation.  
- **Multi-OS Support:** Improve compatibility for Mac/Linux.  
- **Security:** Add JWT/OAuth for API endpoints.  
- **UI Dashboard:** Web interface for log monitoring.  
```