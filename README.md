# Resume Optimizer

A simple, production-grade resume optimization web application using GPT-3.5 Turbo. This application helps users optimize their resumes for specific job descriptions using AI-generated suggestions.

## Project Structure

```
resume-optimizer/
├── lambda_function/
│   ├── app.py           # Lambda function handler
│   ├── utils.py         # Helper functions for OpenAI API
│   └── requirements.txt # Dependencies for Lambda deployment
├── frontend/
│   ├── index.html       # User interface
│   ├── style.css        # Styling
│   └── script.js        # Client-side functionality
└── .env                 # Environment variables (create manually)
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r lambda_function/requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. Test the Lambda function locally:
   ```
   cd lambda_function
   python app.py
   ```

### AWS Deployment

1. Package the Lambda function:
   ```
   # Windows
   mkdir package
   pip install -r lambda_function/requirements.txt -t ./package
   copy lambda_function\app.py package\
   copy lambda_function\utils.py package\
   cd package
   powershell Compress-Archive -Path * -DestinationPath ..\lambda_deployment.zip
   
   # Linux/Mac
   mkdir package
   pip install -r lambda_function/requirements.txt -t ./package
   cp lambda_function/app.py lambda_function/utils.py package/
   cd package
   zip -r ../lambda_deployment.zip .
   ```

2. Manual AWS Setup:
   - Create a Lambda function in the AWS Console
   - Upload the `lambda_deployment.zip` file
   - Set the handler to `app.handler`
   - Add an environment variable: `OPENAI_API_KEY` with your API key
   - Create an API Gateway trigger
   - Configure the API Gateway to use Lambda Proxy integration
   - Deploy the API Gateway

3. Update the frontend:
   - Open `frontend/script.js`
   - Replace the `API_ENDPOINT` value with your API Gateway URL

### Frontend Deployment

1. Create an S3 bucket in the AWS Console
2. Enable static website hosting
3. Upload the frontend files (`index.html`, `style.css`, `script.js`)
4. Set the bucket policy to allow public read access
5. Access your website using the S3 website endpoint URL

## Usage

1. Enter your resume text in the first text area
2. Enter the job description in the second text area
3. Click "Optimize Resume"
4. View the AI-generated suggestions for improving your resume

## Testing

You can test the API endpoint using curl or Postman:

```
curl -X POST https://your-api-gateway-url/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "resumeText": "Software Engineer with 5 years of experience in Python and JavaScript.",
    "jobDescription": "Looking for a Senior Software Engineer with Python, AWS, and React experience."
  }'
```