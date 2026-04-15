from prompts.match_prompt import match_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.0)

match_chain = match_prompt | llm