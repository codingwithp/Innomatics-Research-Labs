from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
Compare resume with job description.

Resume Data:
{resume_data}

Job Description:
{job_description}

STRICT RULES:
- Return ONLY JSON
- No explanation

Format:
{{
  "matching_skills": [],
  "missing_skills": []
}}
"""
)