from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["match_data", "score"],
    template="""
Explain the score.

Match Data:
{match_data}

Score:
{score}

Rules:
- Be concise
- Mention strengths
- Mention missing skills
- No hallucination
"""
)