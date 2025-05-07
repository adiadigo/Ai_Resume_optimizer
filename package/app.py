"""
Resume Optimizer Lambda Function

This module serves as the entry point for the AWS Lambda function that processes
resume optimization requests using OpenAI's GPT-3.5 Turbo API.

For local testing:
- Run this file directly with Python
- Use a tool like Postman to send POST requests to http://localhost:8000/optimize

For deployment:
- Zip this file along with utils.py and the site-packages directory
- Upload to AWS Lambda
- Configure API Gateway to trigger this Lambda function
"""

import json
import os
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from dotenv import load_dotenv
from utils import optimize_resume

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Resume Optimizer API")

# Define request model
class OptimizeRequest(BaseModel):
    resumeText: str
    jobDescription: str

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    """
    Endpoint to optimize a resume based on a job description.
    
    Args:
        request: Contains resumeText and jobDescription fields
        
    Returns:
        JSON response with optimized resume suggestions
    """
    try:
        # Validate inputs
        if not request.resumeText or not request.jobDescription:
            raise HTTPException(status_code=400, detail="Resume text and job description are required")
        
        # Process the optimization request
        result = optimize_resume(request.resumeText, request.jobDescription)
        
        # Return the result
        return {"success": True, "suggestions": result}
    
    except Exception as e:
        # Log the error (would be captured in CloudWatch)
        print(f"Error: {str(e)}")
        return {"success": False, "error": str(e)}

# Create a handler for AWS Lambda
handler = Mangum(app)

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Sample test with curl (for local testing):

curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "resumeText": "Software Engineer with 5 years of experience in Python and JavaScript.",
    "jobDescription": "Looking for a Senior Software Engineer with Python, AWS, and React experience."
  }'
"""