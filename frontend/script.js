/**
 * Resume Optimizer - Frontend JavaScript
 * 
 * This script handles the form submission, API communication,
 * and displaying results for the Resume Optimizer application.
 */

// API Gateway endpoint URL - Replace with your actual API Gateway URL after deployment
const API_ENDPOINT = 'https://m6g3p7r95e.execute-api.us-east-1.amazonaws.com/default/ResumeOptimizer';

// DOM elements
const form = document.getElementById('optimizerForm');
const submitBtn = document.getElementById('submitBtn');
const resultsContainer = document.getElementById('resultsContainer');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultContent = document.getElementById('resultContent');

/**
 * Initialize the application
 */
function init() {
    // Add event listeners
    form.addEventListener('submit', handleFormSubmit);
    
    // Hide results container initially
    resultsContainer.style.display = 'none';
}

/**
 * Handle form submission
 * @param {Event} event - The form submission event
 */
async function handleFormSubmit(event) {
    // Prevent default form submission
    event.preventDefault();
    
    // Get form data
    const resumeText = document.getElementById('resumeText').value.trim();
    const jobDescription = document.getElementById('jobDescription').value.trim();
    
    // Validate inputs
    if (!resumeText || !jobDescription) {
        alert('Please enter both your resume and the job description.');
        return;
    }
    
    try {
        // Show loading state
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

/**
 * Send optimization request to the API
 * @param {string} resumeText - The resume text
 * @param {string} jobDescription - The job description text
 * @returns {Promise<Object>} - The API response
 */
async function sendOptimizationRequest(resumeText, jobDescription) {
    // Prepare request payload
    const payload = {
        resumeText,
        jobDescription
    };
    
    // Send request to API
    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    // Check if response is ok
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to optimize resume');
    }
    
    // Parse and return response data
    return await response.json();
}

/**
 * Display optimization results
 * @param {Object} response - The API response
 */
function displayResults(response) {
    // Show results container
    resultsContainer.style.display = 'block';
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
    
    // Display suggestions
    resultContent.innerHTML = formatSuggestions(response.suggestions);
}

/**
 * Format suggestions for display
 * @param {string} suggestions - The raw suggestions text
 * @returns {string} - Formatted HTML
 */
function formatSuggestions(suggestions) {
    // Convert line breaks to HTML and return
    return suggestions
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

/**
 * Handle API request errors
 * @param {Error} error - The error object
 */
function handleError(error) {
    // Show results container
    resultsContainer.style.display = 'block';
    
    // Display error message
    resultContent.innerHTML = `
        <div class="error-message">
            <p>Sorry, an error occurred while processing your request:</p>
            <p>${error.message || 'Unknown error'}</p>
            <p>Please try again later or contact support.</p>
        </div>
    `;
    
    // Log error to console
    console.error('Optimization error:', error);
}

/**
 * Show or hide loading indicator
 * @param {boolean} isLoading - Whether loading is in progress
 */
function showLoading(isLoading) {
    // Update button state
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Processing...' : 'Optimize Resume';
    
    // Show/hide loading indicator
    loadingIndicator.style.display = isLoading ? 'block' : 'none';
    
    // Hide/show result content
    resultContent.style.display = isLoading ? 'none' : 'block';
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);