from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
Assign a score (0-100).

Rules:
- More matching skills = higher score
- More missing skills = lower score

STRICT RULES:
- Return ONLY JSON
- No explanation

Match Data:
{match_data}

Format:
{{
  "score": number
}}
"""
)