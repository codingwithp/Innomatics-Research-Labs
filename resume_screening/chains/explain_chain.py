from prompts.explain_prompt import explain_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.3)

explain_chain = explain_prompt | llm