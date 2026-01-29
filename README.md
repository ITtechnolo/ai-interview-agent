# AI Interview Prep Agent (LangGraph + Gemini)

A smart, interactive CLI agent that generates tailored interview questions and answers based on a job role and experience level. Powered by **LangGraph** and **Google's Gemini API**.

## 🚀 Features
- **Dynamic Question Generation**: Creates unique questions based on the specific job role (e.g., "Python Developer") and experience level (e.g., "Junior", "Senior").
- **AI-Powered Answers**: Generates concise, model answers to help you prepare.
- **Robust Output**: Automatically handles structured data from the API to ensure clean, readable text.
- **Free to Use**: Optimized for the free tier of the Google Gemini API.

## 🛠️ Tech Stack
- **Python 3.10+**
- **LangGraph**: For managing the agent's state and workflow.
- **LangChain**: For LLM orchestration.
- **Google Gemini**: The underlying Large Language Model (LLM).

## 📋 Prerequisites
- A Google Cloud API Key (Free). Get one [here](https://aistudio.google.com/app/apikey).
- Python installed on your machine.

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ITtechnolo/ai-interview-agent.git
    cd ai-interview-agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install langgraph langchain-google-genai langchain-core python-dotenv
    ```

3.  **Configure Environment**:
    - Create a `.env` file in the root directory.
    - Add your Google API Key:
      ```env
      GOOGLE_API_KEY=your_api_key_here
      ```

##  ▶️ Usage

Run the agent from your terminal:

```bash
python -u interview_agent.py
```

Follow the prompts:
1.  Enter the **Job Role** (e.g., `Data Scientist`).
2.  Enter the **Experience Level** (e.g., `Senior`).

The agent will generate 3 relevant questions and provide concise answers for each.

## 🐛 Troubleshooting
- **429 Resource Exhausted**: If you hit the free tier limit, wait a minute and try again. The script is configured to use `gemini-flash-latest` which is generally efficient.
- **Output Issues**: If the output seems stuck, use the `-u` flag (`python -u interview_agent.py`) to force unbuffered output.

## 📄 License
This project is open-source and available under the MIT License.