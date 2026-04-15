from prompts.extract_prompt import extract_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.0)

extract_chain = extract_prompt | llm