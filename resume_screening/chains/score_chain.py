from prompts.score_prompt import score_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.0)

score_chain = score_prompt | llm