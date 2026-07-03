import json
from app.services.llm.llm_service import llm
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an expert educator.

Analyze the following text chunk.

Extract the 5 most important SPECIFIC concepts,
technologies, models, mechanisms, protocols,
architectures, or subtopics.

Rules:

- Prefer specific concepts over broad subjects.
- Avoid generic topics such as:
  "Introduction",
  "Overview",
  "Definition",
  "Basics",
  "Cloud Computing",
  "Java",
  "Database Management System".
- Prefer:
  "Virtualization",
  "Auto Scaling",
  "Load Balancing",
  "Inheritance",
  "Polymorphism",
  "B+ Tree",
  "Normalization".
- Topic names should be concise.
- Each topic should represent a concept that could be asked in an exam question.
- Assign importance from 1 to 10.

Return ONLY valid JSON.

Example:

[
  {{
    "topic": "Virtualization",
    "importance": 9
  }},
  {{
    "topic": "Auto Scaling",
    "importance": 8
  }}
]

Text:
{chunk}
""")



def extract_topics(chunk: str):

    chain = prompt | llm

    response = chain.invoke({
        "chunk": chunk
    })

    return json.loads(response.content)