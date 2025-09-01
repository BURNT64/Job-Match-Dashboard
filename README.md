# Job Match Dashboard

A simple tool that compares a candidate's CV against a job description to highlight matching and missing skills.  
Built with **Python**, **scikit-learn**, and **Streamlit**.

---

## Features
- Upload a CV (PDF or DOCX)
- Paste a job description
- Get a **match score (%)**
- See **top matching skills** and **missing keywords**
- Visualize results with charts

---

## Installation
1) Clone the repository:
   git clone https://github.com/your-username/job-match-dashboard.git
   cd job-match-dashboard

2) Create a virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate    # Mac/Linux
   venv\Scripts\activate       # Windows
   pip install -r requirements.txt

---

## Usage
1) Run the app locally:
   streamlit run app.py

---
## Example

CV: Python developer with experience in SQL and data analysis

JD: Looking for a software engineer with Python, SQL, and machine learning skills

Output:
Match Score: 67%
Matching Skills: Python, SQL
Missing Skills: Machine Learning
