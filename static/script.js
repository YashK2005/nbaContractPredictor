// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading state
function setLoading(isLoading) {
    const submitBtn = document.getElementById('submit-btn');
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.value = 'Predicting...';
    } else {
        submitBtn.disabled = false;
        submitBtn.value = 'Predict Salary';
    }
}

// Handle form submission
document.getElementById('prediction-form').addEventListener('submit', function(e) {
    setLoading(true);
});

// Handle player not found error
window.addEventListener('DOMContentLoaded', function() {
    if (playerNotFound) {
        const playerInput = document.getElementById('player_name');
        playerInput.classList.add('error');
        setTimeout(() => {
            playerInput.classList.remove('error');
        }, 3000);
    }
});

// Enhanced autocomplete functionality
const playerInput = document.getElementById('player_name');
const suggestionsDiv = document.getElementById('autocomplete-suggestions');

// Show suggestions
function showSuggestions(suggestions) {
    suggestionsDiv.innerHTML = '';
    
    if (!suggestions || suggestions.length === 0) {
        suggestionsDiv.innerHTML = '<div class="no-results">No players found</div>';
        return;
    }

    suggestions.forEach(function(name) {
        const suggestionDiv = document.createElement('div');
        suggestionDiv.className = 'suggestion-item';
        suggestionDiv.textContent = name;
        suggestionDiv.addEventListener('click', function() {
            playerInput.value = name;
            suggestionsDiv.style.display = 'none';
            playerInput.focus();
            document.getElementById('prediction-form').submit();
        });
        suggestionsDiv.appendChild(suggestionDiv);
    });
}

// Handle input changes
playerInput.addEventListener('input', debounce(function() {
    const inputVal = this.value.trim();
    
    if (inputVal.length > 0) {
        // Show loading state
        suggestionsDiv.innerHTML = '<div class="loading">Searching...</div>';
        suggestionsDiv.style.display = 'block';
        
        // Fetch suggestions
        fetch(`/autocomplete?query=${encodeURIComponent(inputVal)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                showSuggestions(data);
            })
            .catch(error => {
                console.error('Error:', error);
                suggestionsDiv.innerHTML = '<div class="error">Error fetching suggestions</div>';
            });
    } else {
        suggestionsDiv.style.display = 'none';
    }
}, 300));

// Close suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!playerInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
        suggestionsDiv.style.display = 'none';
    }
});

// Handle keyboard navigation
playerInput.addEventListener('keydown', function(e) {
    const suggestions = suggestionsDiv.getElementsByClassName('suggestion-item');
    
    if (suggestions.length === 0) return;

    if (e.key === 'ArrowDown' && document.activeElement === this) {
        e.preventDefault();
        suggestions[0].focus();
    } else if (e.key === 'ArrowUp' && document.activeElement === suggestions[0]) {
        e.preventDefault();
        this.focus();
    } else if (e.key === 'Enter' && document.activeElement !== this) {
        e.preventDefault();
        document.activeElement.click();
    } else if (e.key === 'Escape') {
        suggestionsDiv.style.display = 'none';
    }
});
