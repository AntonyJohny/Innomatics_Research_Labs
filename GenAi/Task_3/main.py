from chains.screening_chain import get_screening_chain

# Example Data
job_desc = "Data Scientist: Requires Python, SQL, and 2 years Machine Learning experience."

resumes = [
    "Expert: 5 years Python, SQL, Scikit-learn, built 10 ML models.", # Strong
    "Junior: Knows Python and basic Excel. No ML experience.",       # Average/Weak
    "Chef: 10 years cooking Italian cuisine. Skills: Pizza, Pasta."   # Weak
]

chain = get_screening_chain()

for i, resume in enumerate(resumes):
    print(f"--- Running Case {i+1} ---")
    response = chain.invoke({
        "job_description": job_desc,
        "resume_text": resume
    })
    print(response.content)