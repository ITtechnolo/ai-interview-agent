import os
from typing import List, TypedDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for API key
if not os.environ.get("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY not found in environment or .env file.")
    print("Please add your key to the .env file.")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

# --- 1. Setup ---
# Initialize the Gemini LLM
# Ensure you have installed: pip install langchain-google-genai python-dotenv langgraph
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.7)

# --- 2. Define State ---
class InterviewState(TypedDict):
    job_role: str
    experience_level: str
    questions: List[str]
    answers: List[str]

# --- 3. Define Nodes ---

# --- 3. Define Nodes ---

def extract_text(content):
    """Helper to extract text from LLM response, handling both string and list formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle case where content is a list of dicts (e.g. Gemini structured output)
        text_parts = []
        for part in content:
            if isinstance(part, dict) and 'text' in part:
                text_parts.append(part['text'])
            elif isinstance(part, str):
                text_parts.append(part)
        return "".join(text_parts)
    return str(content)

def generate_questions(state: InterviewState):
    """Generates interview questions based on role and experience."""
    print(f"\n--- Generating questions for a {state['experience_level']} {state['job_role']} ---")
    
    prompt = ChatPromptTemplate.from_template(
        "Generate 3 interview questions for a {experience_level} {job_role}. "
        "Return just the questions as a numbered list."
    )
    chain = prompt | llm
    response = chain.invoke({"job_role": state["job_role"], "experience_level": state["experience_level"]})
    
    questions_text = extract_text(response.content)
    # Basic parsing to handle numbered lists
    questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
    
    return {"questions": questions}

def generate_answers(state: InterviewState):
    """Generates short answers for the questions."""
    print("--- Generating answers ---")
    questions = state["questions"]
    answers = []
    
    for q in questions:
        prompt = ChatPromptTemplate.from_template(
            "Provide a short, concise answer to this interview question: {question}"
        )
        chain = prompt | llm
        response = chain.invoke({"question": q})
        answers.append(extract_text(response.content))
        
    return {"answers": answers}

def print_results(state: InterviewState):
    """Formats and prints the final output."""
    print("\n=== Interview Prep Results ===\n")
    questions = state["questions"]
    answers = state["answers"]
    
    # Handle cases where parsing might have left extra lines
    # Only zip up to the length of the shortest list to avoid errors
    for i, (q, a) in enumerate(zip(questions, answers)):
        print(f"Q: {q}")
        print(f"A: {a}\n")
    
    return {}

# --- 4. Build Graph ---
builder = StateGraph(InterviewState)

builder.add_node("generate_questions", generate_questions)
builder.add_node("generate_answers", generate_answers)
builder.add_node("print_results", print_results)

builder.add_edge(START, "generate_questions")
builder.add_edge("generate_questions", "generate_answers")
builder.add_edge("generate_answers", "print_results")
builder.add_edge("print_results", END)

graph = builder.compile()

# --- 5. Execution ---
if __name__ == "__main__":
    print("Welcome to the AI Interview Prep Agent (Powered by Gemini)!")
    
    role = input("Enter the job role (e.g., Python Developer): ") or "Python Developer"
    level = input("Enter experience level (e.g., Junior, Senior): ") or "Junior"
    
    initial_state = {"job_role": role, "experience_level": level, "questions": [], "answers": []}
    
    try:
        graph.invoke(initial_state)
    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Tip: Make sure your GOOGLE_API_KEY is correct and you have internet access.")
