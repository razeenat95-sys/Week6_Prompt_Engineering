# Week 6 – Prompt Engineering

## Task
Designing Effective Prompts for Large Language Models.

## Objective
This project demonstrates how Zero-shot, One-shot, Few-shot, Role Prompting, and Chain-of-Thought-style structured prompting affect LLM responses.

## Folder structure
```text
Prompt_Engineering/
├── dataset/
│   ├── prompts.csv
│   ├── generated_responses.csv
│   ├── prompt_comparison.csv
│   └── evaluation_results.csv
├── notebook/
│   └── Week6_Prompt_Engineering.ipynb
├── prompt_engineering.py
├── prompt_templates.md
├── README.md
├── requirements.txt
└── .gitignore
```

## How to run in VS Code

1. Extract this folder.
2. Open the **Prompt_Engineering** folder in VS Code.
3. Open a new terminal.
4. Create/activate a virtual environment if you normally use one.
5. Install packages:

```bash
pip install -r requirements.txt
```

6. Run the complete project:

```bash
python prompt_engineering.py
```

The first run downloads `google/flan-t5-small` from Hugging Face, so internet is required and the first run may take a few minutes.

7. Open:
`notebook/Week6_Prompt_Engineering.ipynb`

Select the same Python environment and run the notebook cells from top to bottom.

## Submission files
The important submission artifacts are:
- `notebook/Week6_Prompt_Engineering.ipynb`
- `dataset/prompts.csv`
- `dataset/generated_responses.csv`
- `dataset/prompt_comparison.csv`
- `dataset/evaluation_results.csv`
- `prompt_engineering.py`
- `prompt_templates.md`
- `README.md`
- `requirements.txt`

## Note
The healthcare and finance examples are educational demonstrations, not professional medical or financial advice. The evaluation CSV uses a simple automated rubric and should be treated as supporting analysis rather than a definitive human evaluation.
