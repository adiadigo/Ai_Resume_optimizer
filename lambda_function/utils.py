"""
Utility functions for the Resume Optimizer application.

This module contains helper functions for interacting with the OpenAI API
and processing resume optimization requests.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt template function for formatting the optimization instructions
prompt_template = lambda resume_string, jd_string: f"""
You are a professional resume optimization expert specializing in tailoring \
resumes to specific job descriptions. Your goal is to optimize my resume and \
provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the \
job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and \
**targeted** resume.  
   - Limit work experience section to 2-3 most relevant roles  
   - Limit bullet points under each role to 2-3 most relevant impacts  

2. **Action-Driven Results**:  
   - Use **strong action verbs** and **quantifiable results** (e.g., \
percentages, revenue, efficiency improvements) to highlight impact.  

3. **Keyword Optimization**:  
   - Integrate **keywords** and phrases from the job description naturally to \
optimize for ATS (Applicant Tracking Systems).  

4. **Additional Suggestions** *(If Gaps Exist)*:  
   - If the resume does not fully align with the job description, suggest:  
     1. **Additional technical or soft skills** that I could add to make my \
profile stronger.  
     2. **Certifications or courses** I could pursue to bridge the gap.  
     3. **Project ideas or experiences** that would better align with the role.  

5. **Formatting**:  
   - Output the tailored resume in **clean Markdown format**.  
   - Include an **"Additional Suggestions"** section at the end with \
actionable improvement recommendations.  

---

### Input:
- **My resume**:  
{resume_string}

- **The job description**:  
{jd_string}

---

### Output:  
1. **Tailored Resume**:  
   - A resume in **Markdown format** that emphasizes relevant experience, \
skills, and achievements.  
   - Incorporates job description **keywords** to optimize for ATS.  
   - Uses strong language and is no longer than **one page**.

2. **Additional Suggestions** *(if applicable)*:  
   - List **skills** that could strengthen alignment with the role.  
   - Recommend **certifications or courses** to pursue.  
   - Suggest **specific projects or experiences** to develop.
"""

def optimize_resume(resume_text, job_description):
    """
    Optimize a resume based on a job description using OpenAI's GPT-3.5 Turbo.

    Args:
        resume_text (str): The user's current resume text
        job_description (str): The job description text

    Returns:
        str: AI-generated optimized resume and suggestions
    """
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please check your environment variables.")

    prompt = prompt_template(resume_text, job_description)

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional resume consultant. Your task is to strictly follow the prompt "
                        "and return a Markdown-formatted tailored resume, followed by actionable suggestions."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        raise Exception(f"Failed to process resume: {str(e)}")
