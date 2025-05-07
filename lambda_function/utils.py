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

def optimize_resume(resume_text, job_description):
    """
    Optimize a resume based on a job description using OpenAI's GPT-3.5 Turbo.
    
    Args:
        resume_text (str): The user's current resume text
        job_description (str): The job description text
        
    Returns:
        str: AI-generated suggestions for resume optimization
    """
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please check your environment variables.")
    
    # Construct the prompt for GPT-3.5 Turbo
    prompt = f"""
    You are a professional resume consultant. Your task is to provide specific suggestions to optimize 
    the following resume for the given job description. Focus on:
    
    1. Skills alignment and highlighting relevant experience
    2. Keyword optimization for ATS (Applicant Tracking Systems)
    3. Strengthening impact statements and quantifiable achievements
    4. Removing irrelevant information
    5. Improving overall structure and clarity
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Provide your suggestions in a clear, structured format with specific examples of improvements.
    """
    
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume consultant specializing in optimizing resumes for specific job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        # Extract and return the generated suggestions
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Log the error and re-raise
        print(f"Error calling OpenAI API: {str(e)}")
        raise Exception(f"Failed to process resume: {str(e)}")