# LLM + RAG Function Execution API

## 📖 Overview  
This project combines **Large Language Models (LLMs)** with **Retrieval-Augmented Generation (RAG)** to understand natural language commands (e.g., "Open calculator") and execute predefined Python automation functions. It dynamically generates executable code, matches functions using vector similarity, logs the execution, and exposes everything through a FastAPI server.

---

## 📂 Project Structure  

```text
llm-rag-api/
├── .env                  # Stores Together.ai API key (not committed)
├── main.py               # FastAPI server and endpoint logic
├── function_registry.py  # Automation functions + metadata
├── embeddings.py         # Sentence-transformers embeddings
├── vector_store.py       # FAISS vector database
├── code_generator.py     # Together.ai (Mistral) code generation
├── requirements.txt      # Dependency list
├── logs/                 # Execution logs
└── screenshot/           # Calculator screenshots
```

---

## 🧩 Key Components  

### 1. **Function Registry**
- **File:** `function_registry.py`
- **Functions Included:**
  - `open_calculator()`
  - `open_chrome()`
  - `check_ram_usage()`
  - `run_shell_command()`
- **Metadata:** Stored in `FUNCTIONS_METADATA` for RAG retrieval.

### 2. **Embeddings & Vector Store**
- **Model Used:** `all-MiniLM-L6-v2` from `sentence-transformers`
- **Vector Store:** FAISS for fast similarity search

### 3. **Dynamic Code Generation**
- **Model:** Mistral (via Together.ai)
- **Generated Output Example:**
  ```python
  from function_registry import open_calculator
  open_calculator()
  ```

### 4. **API Service**
- **Framework:** FastAPI  
- **Endpoint:** `/execute` (POST)  
- **Logging:** Logs stored in `logs/app.log`

---

## ⚙️ Setup  

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm-rag-api.git
cd llm-rag-api
```

### 2. Create Virtual Environment

**Conda:**
```bash
conda create -n llm-rag python=3.10
conda activate llm-rag
```

**Virtualenv:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Or with conda:**
```bash
conda install -c conda-forge requests python-dotenv sentence-transformers faiss-cpu fastapi uvicorn psutil
```

### 4. Add Your API Key

Create a `.env` file:

```ini
TOGETHER_API_KEY=your_api_key_here
```

### 5. Run the Server

```bash
uvicorn main:app --reload
```

Visit the interactive docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Usage

### Send a Request

```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Check RAM usage"}'
```

### Example Response

```json
{
  "prompt": "Check RAM usage",
  "matched_function": "check_ram_usage",
  "execution_result": "RAM usage: 45%",
  "generated_code_snippet": "from function_registry import check_ram_usage\ncheck_ram_usage()"
}
```

---

## 💡 Example Input/Output

**Input:**

```json
{ "prompt": "Open calculator" }
```

**Output:**

```json
{
  "prompt": "Open calculator",
  "matched_function": "open_calculator",
  "execution_result": "Function executed successfully",
  "generated_code_snippet": "from function_registry import open_calculator\nopen_calculator()"
}
```

When you submit the prompt `"Open calculator"`, the API recognizes and executes the corresponding function on your local system, which launches the default Calculator app.

---

## 🖼️ Screenshots

Below are four screenshots demonstrating how this API works when sending a prompt to open the calculator:

| Step                 | Screenshot                       | Description                                                                     |
|----------------------|----------------------------------|---------------------------------------------------------------------------------|
| **1**               | ![](screenshot/1.png)            | FastAPI docs UI showing the `/execute` endpoint.                               |
| **2**               | ![](screenshot/2.png)            | Submitting the JSON request body with `"prompt": "Open calculator"`.           |
| **3**               | ![](screenshot/3.png)            | The running Windows Calculator after the function was executed successfully.    |
| **4**               | ![](screenshot/4.png)            | Response body in the docs, showing the matched function and success message.    |

---

## 🔮 Future Enhancements  
- Add more functions: file operations, email automation, browser actions  
- Add multi-OS support (Linux, MacOS)  
- Add authentication (JWT/OAuth)  
- Create a web dashboard to monitor logs and executions
