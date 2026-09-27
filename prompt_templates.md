# Reusable Prompt Templates

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
