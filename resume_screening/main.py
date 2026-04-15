
import json
from chains.extract_chain import extract_chain
from chains.match_chain import match_chain
from chains.score_chain import score_chain
from chains.explain_chain import explain_chain

job_description = """
Looking for Data Scientist with:
- Python
- Machine Learning
- SQL
- Deep Learning
"""

resumes = {
    "Strong Candidate": """
    Data Scientist with 3 years experience.
    Skilled in Python, Machine Learning, SQL, Deep Learning.
    Worked with TensorFlow and PyTorch.
    """,

    "Average Candidate": """
    Python developer with 2 years experience.
    Worked on SQL and basic machine learning models.
    Used TensorFlow.
    """,

    "Weak Candidate": """
    Frontend developer.
    Skills: HTML, CSS, JavaScript.
    No experience in data science.
    """
}

for label, resume in resumes.items():
    print(f"\n===== {label} =====")

    # Step 1: Extract
    extract_output = extract_chain.invoke({"resume": resume}).content
    print("\nExtracted:\n", extract_output)

    # Step 2: Match
    match_output = match_chain.invoke({
        "resume_data": extract_output,
        "job_description": job_description
    }).content
    print("\nMatch:\n", match_output)

    # Step 3: Score
    score_output = score_chain.invoke({
        "match_data": match_output
    }).content
    print("\nScore:\n", score_output)

    # Step 4: Explain
    explain_output = explain_chain.invoke({
        "match_data": match_output,
        "score": score_output
    }).content
    print("\nExplanation:\n", explain_output)
