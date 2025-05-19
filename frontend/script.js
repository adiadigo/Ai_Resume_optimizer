

const API_ENDPOINT = 'https://m6g3p7r95e.execute-api.us-east-1.amazonaws.com/prod/ResumeOptimizer';

const form = document.getElementById('optimizerForm');
const submitBtn = document.getElementById('submitBtn');
const resultsContainer = document.getElementById('resultsContainer');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultContent = document.getElementById('resultContent');

function init() {
    form.addEventListener('submit', handleFormSubmit);
    
    resultsContainer.style.display = 'none';
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const resumeText = document.getElementById('resumeText').value.trim();
    const jobDescription = document.getElementById('jobDescription').value.trim();
    
    if (!resumeText || !jobDescription) {
        alert('Please enter both your resume and the job description.');
        return;
    }
    
    try {
        showLoading(true);
        
        // Send request to API
        const response = await sendOptimizationRequest(resumeText, jobDescription);
        
        // Display results
        displayResults(response);
    } catch (error) {
        // Handle errors
        handleError(error);
    } finally {
        // Hide loading state
        showLoading(false);
    }
}

async function sendOptimizationRequest(resumeText, jobDescription) {
    const payload = {
        resumeText,
        jobDescription
    };
    
    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to optimize resume');
    }
    
    return await response.json();
}

function displayResults(response) {
    resultsContainer.style.display = 'block';
    
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
    
    resultContent.innerHTML = formatSuggestions(response.suggestions);
}

function formatSuggestions(suggestions) {
    return suggestions
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function handleError(error) {
    resultsContainer.style.display = 'block';
    
    resultContent.innerHTML = `
        <div class="error-message">
            <p>Sorry, an error occurred while processing your request:</p>
            <p>${error.message || 'Unknown error'}</p>
            <p>Please try again later or contact support.</p>
        </div>
    `;
    
    console.error('Optimization error:', error);
}

function showLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Processing...' : 'Optimize Resume';
    
    loadingIndicator.style.display = isLoading ? 'block' : 'none';
    
    resultContent.style.display = isLoading ? 'none' : 'block';
}

document.addEventListener('DOMContentLoaded', init);
