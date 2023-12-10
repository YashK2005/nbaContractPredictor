window.addEventListener('DOMContentLoaded', function() {
    if(player_not_found) {
        alert('Player not found. Please check the player name.');
    }
});

document.getElementById('player_name').addEventListener('input', function() {
    var inputVal = this.value;
    var suggestionsDiv = document.getElementById('autocomplete-suggestions');

    if(inputVal.length > 0) {
        fetch(`/autocomplete?query=${encodeURIComponent(inputVal)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsDiv.innerHTML = '';
                
                data.forEach(function(name) {
                    var words = name.split(' ');
                    var highlightedName = words.map(function(word) {
                        // Check if the word starts with the input value
                        if (word.toLowerCase().startsWith(inputVal)) {
                            // Bold only the matching part
                            return '<strong>' + word.substr(0, inputVal.length) + '</strong>' + word.substr(inputVal.length);
                        } else {
                            return word;
                        }
                    }).join(' ');
                    var suggestionDiv = document.createElement('div');
                    suggestionDiv.innerHTML = highlightedName;
                    suggestionDiv.addEventListener('click', function() {
                        document.getElementById('player_name').value = name;
                        suggestionsDiv.innerHTML = '';
                        document.querySelector('form').submit(); // Submit the form
                    });
                    suggestionsDiv.appendChild(suggestionDiv);
                });
            });
    } else {
        suggestionsDiv.innerHTML = '';
    }
});