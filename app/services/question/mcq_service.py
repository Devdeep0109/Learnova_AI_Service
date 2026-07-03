from app.services.llm.llm_service import llm
from langchain_core.prompts import ChatPromptTemplate
import json
from app.utils.logger import logger


prompt = ChatPromptTemplate.from_template("""
You are an experienced university professor and assessment designer.

Your task is to generate {question_count} high-quality multiple-choice questions (MCQs).

==================================================
TOPIC
==================================================

{topic}

==================================================
DIFFICULTY
==================================================

{difficulty}

Difficulty Guidelines:

Easy:
- Definition based
- Recall and basic understanding
- Direct concept identification

Medium:
- Conceptual understanding
- Comparison between concepts
- Interpretation and reasoning

Hard:
- Scenario-based
- Real-world application
- Architecture
- Troubleshooting
- Multi-step reasoning
- Analytical thinking

==================================================
SOURCE CONTENT
==================================================

{content}

==================================================
PREVIOUSLY GENERATED QUESTIONS
==================================================

{previous_questions}

==================================================
QUESTION GENERATION RULES
==================================================

1. Every question MUST primarily assess the given topic.

2. Use the provided source content as the PRIMARY source of knowledge.

3. If the source content is insufficient to generate diverse questions,
   expand using your own domain knowledge ONLY about the SAME topic.

4. Never introduce unrelated concepts.

5. Related topics may appear only as supporting context,
   but the primary focus must always remain the given topic.

6. Do NOT repeat previously generated questions.

7. Do NOT repeat the same concept even if the wording is different.

8. If a definition has already been covered,
   generate questions on:
   - Applications
   - Architecture
   - Advantages
   - Disadvantages
   - Comparisons
   - Scenarios
   - Troubleshooting
   - Best Practices
   - Real-world use cases

9. Ensure every question covers a different aspect of the topic.

10. Every question should have exactly ONE primary learning objective.

11. Avoid trivial or overly obvious questions.

12. Avoid ambiguous questions.

13. Avoid "All of the above".

14. Avoid "None of the above".

==================================================
QUESTION QUALITY
==================================================

Every question must:

✓ Test conceptual understanding.

✓ Be factually correct.

✓ Have exactly FOUR options.

✓ Have ONLY ONE correct answer.

✓ Have plausible distractors.

✓ Include a concise explanation describing why the answer is correct.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT return code blocks.

Do NOT include any explanation outside the JSON.

Return the following format exactly:

[
  {{
    "question": "...",
    "options": [
      "...",
      "...",
      "...",
      "..."
    ],
    "answer": "A",
    "explanation": "..."
  }}
]
""")

def generate_mcqs(
    topic,
    content,
    question_count,
    difficulty,
    previous_questions
):

    logger.info(
        f"Generating {question_count} MCQs for topic '{topic}' "
        f"with difficulty '{difficulty}'."
    )

    chain = prompt | llm

    history = (
        "\n\n".join(
            f"{index + 1}. {question}"
            for index, question in enumerate(previous_questions)
        )
        if previous_questions
        else "None"
    )

    try:

        response = chain.invoke(
            {
                "topic": topic,
                "content": content,
                "question_count": question_count,
                "difficulty": difficulty,
                "previous_questions": history
            }
        )

        mcqs = json.loads(
            response.content
        )

        logger.info(
            f"Successfully generated {len(mcqs)} MCQs for topic '{topic}'."
        )

        return mcqs

    except json.JSONDecodeError:

        logger.exception(
            f"LLM returned invalid JSON for topic '{topic}'."
        )

        raise

    except Exception:

        logger.exception(
            f"Failed to generate MCQs for topic '{topic}'."
        )

        raise