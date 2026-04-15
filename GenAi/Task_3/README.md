# AI Resume Screening System with Tracing

An AI-powered tool built during my GenAI Internship at Innomatics Research Lab. This system evaluates resumes against job descriptions using LangChain and provides explainable scoring.

## 🚀 Features
- **Skill Extraction:** Automatically identifies skills, experience, and tools from resumes.
- **Matching Logic:** Compares candidate profiles against specific Job Descriptions.
- **Explainable AI:** Provides a fit score (0-100) with detailed reasoning for the grade.
- **LangSmith Tracing:** Full observability of the LLM pipeline for debugging and monitoring.

## 🛠️ Tech Stack
- **Framework:** LangChain (LCEL)
- **LLM:** Groq (Llama 3.3 70B)
- **Monitoring:** LangSmith
- **Environment:** Python 3.11+

## 📋 Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `.\venv\Scripts\Activate.ps1`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Create a `.env` file based on `.env.example` and add your API keys.
6. Run the application: `python main.py`.
