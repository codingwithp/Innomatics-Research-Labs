from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are a resume parser.

Extract ONLY the following:
- skills
- experience
- tools

Resume:
{resume}

STRICT RULES:
- Do NOT assume anything
- Return ONLY JSON
- No explanation, no extra text

Format:
{{
  "skills": [],
  "experience": "",
  "tools": []
}}
"""
)