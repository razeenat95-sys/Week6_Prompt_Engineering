"""
Week 6 - Prompt Engineering
Designing Effective Prompts for Large Language Models

Run:
    python prompt_engineering.py

The script:
1. Loads a pre-trained Hugging Face model.
2. Creates Zero-shot, One-shot, Few-shot, Role, and concise CoT prompts.
3. Generates responses for five real-world problems.
4. Saves all responses and evaluation tables as CSV files.
5. Creates reusable prompt templates.
"""

from pathlib import Path
import csv
import re

MODEL_NAME = "google/flan-t5-small"
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

PROBLEMS = [
    (1, "Education", "A student has difficulty understanding photosynthesis. Explain it simply and give three key points to remember."),
    (2, "Healthcare", "A patient asks what they should do for a mild headache. Give general, safe information and mention when professional medical advice is appropriate."),
    (3, "Finance", "A young adult wants to start budgeting with a monthly income of 30000 rupees. Suggest a simple budgeting approach."),
    (4, "Customer Support", "A customer says their online order has not arrived even though the tracking page says delivered. Write a helpful support response."),
    (5, "Programming", "Explain the difference between a Python list and a tuple to a beginner, with a small example."),
]

def load_model():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise SystemExit(
            "Transformers is not installed. Run: pip install -r requirements.txt"
        ) from exc

    print(f"Loading Hugging Face model: {MODEL_NAME}")
    return pipeline("text2text-generation", model=MODEL_NAME)

def build_prompts(problem):
    return {
        "Zero-shot": (
            f"Answer the following question clearly and accurately for a beginner.\n"
            f"Question: {problem}"
        ),
        "One-shot": (
            "Example:\n"
            "Question: Explain a computer concept to a beginner.\n"
            "Answer: Use simple language, define the concept, and give one small example.\n\n"
            f"Now answer this question in the same style:\n{problem}"
        ),
        "Few-shot": (
            "Example 1: Question: What is evaporation?\n"
            "Answer: Evaporation is when a liquid changes into a gas, usually because of heat.\n\n"
            "Example 2: Question: What is a variable in programming?\n"
            "Answer: A variable is a named place used to store a value, such as age = 20.\n\n"
            f"Now answer this question using the same clear style:\n{problem}"
        ),
        "Role": (
            "Act as a helpful, ethical domain expert. Explain the answer clearly, avoid unnecessary jargon, "
            "and give practical information while noting important limitations.\n"
            f"Question: {problem}"
        ),
        "Chain-of-Thought": (
            "Solve the problem carefully. Organize the answer as: (1) identify the main issue, "
            "(2) give the key reasoning or considerations briefly, and (3) provide the final practical answer. "
            "Do not reveal private hidden reasoning.\n"
            f"Question: {problem}"
        ),
    }

def generate(model, prompt, max_new_tokens=180):
    result = model(prompt, max_new_tokens=max_new_tokens, do_sample=False)
    return result[0]["generated_text"].strip()

def score_response(response, domain):
    text = response.strip()
    words = re.findall(r"\b\w+\b", text)
    length_score = 1 if len(words) >= 25 else 0
    structure_score = 1 if len(text) >= 80 else 0
    domain_terms = {
        "Education": ["student", "plant", "sun", "light", "learn", "photosynthesis"],
        "Healthcare": ["headache", "doctor", "medical", "water", "pain", "advice"],
        "Finance": ["income", "budget", "expense", "save", "saving", "money"],
        "Customer Support": ["order", "delivery", "customer", "tracking", "contact"],
        "Programming": ["list", "tuple", "python", "mutable", "example"],
    }
    hits = sum(term in text.lower() for term in domain_terms.get(domain, []))
    relevance = 2 if hits >= 2 else (1 if hits == 1 else 0)
    clarity = 2 if length_score and structure_score else 1
    accuracy = 2 if hits >= 2 else 1
    completeness = 2 if len(words) >= 45 else 1
    total = relevance + clarity + accuracy + completeness
    return relevance, clarity, accuracy, completeness, total

def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def main():
    DATASET_DIR.mkdir(exist_ok=True)
    model = load_model()

    comparison = []
    evaluations = []
    generated = []

    for problem_id, domain, problem in PROBLEMS:
        print(f"\nProblem {problem_id}: {domain}")
        prompts = build_prompts(problem)
        for technique, prompt in prompts.items():
            print(f"  Generating {technique}...")
            response = generate(model, prompt)
            generated.append([problem_id, technique, response])
            comparison.append([problem_id, domain, technique, response])
            scores = score_response(response, domain)
            evaluations.append([problem_id, domain, technique, *scores, "Automatic rubric; inspect responses manually for final academic evaluation."])

    write_csv(
        DATASET_DIR / "generated_responses.csv",
        ["problem_id", "technique", "response"],
        generated,
    )
    write_csv(
        DATASET_DIR / "prompt_comparison.csv",
        ["problem_id", "domain", "technique", "response"],
        comparison,
    )
    write_csv(
        DATASET_DIR / "evaluation_results.csv",
        ["problem_id", "domain", "technique", "relevance", "clarity", "accuracy", "completeness", "total_score", "notes"],
        evaluations,
    )

    templates = """# Reusable Prompt Templates

## Zero-shot
Answer the following question clearly and accurately for the intended audience:
{question}

## One-shot
Example:
Question: {example_question}
Answer: {example_answer}

Now answer:
{question}

## Few-shot
Example 1:
Q: {example_question_1}
A: {example_answer_1}

Example 2:
Q: {example_question_2}
A: {example_answer_2}

Now answer:
{question}

## Role Prompt
Act as a helpful {role}. Explain the answer clearly, avoid unnecessary jargon, and give practical information.
Question: {question}

## Concise Chain-of-Thought Structure
Solve the problem carefully. Organize the response as:
1. Main issue
2. Key considerations/reasoning summary
3. Final answer
Do not reveal private hidden reasoning.
Question: {question}
"""
    (BASE_DIR / "prompt_templates.md").write_text(templates, encoding="utf-8")

    print("\nProject completed successfully.")
    print("Created:")
    print("  dataset/generated_responses.csv")
    print("  dataset/prompt_comparison.csv")
    print("  dataset/evaluation_results.csv")
    print("  prompt_templates.md")

if __name__ == "__main__":
    main()
