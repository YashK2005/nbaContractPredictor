(function () {
    const routes = new Set(['/', '/how_does_this_work']);

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    function escapeHtml(value) {
        return String(value).replace(/[&<>"']/g, (char) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        }[char]));
    }

    function initPredictor() {
        const playerInput = document.getElementById('player_name');
        const suggestionsDiv = document.getElementById('autocomplete-suggestions');
        const predictionForm = document.getElementById('prediction-form');
        const submitBtn = document.getElementById('submit-btn');
        const resultSlot = document.getElementById('prediction-result');

        if (!playerInput || !suggestionsDiv || !predictionForm || !submitBtn || !resultSlot) {
            return;
        }

        let activeRequest = null;

        function setLoading(isLoading) {
            submitBtn.disabled = isLoading;
            submitBtn.value = isLoading ? 'Running...' : 'Run valuation';
        }

        function closeSuggestions() {
            suggestionsDiv.classList.remove('is-open');
            suggestionsDiv.innerHTML = '';
        }

        function renderStatus(message, className) {
            suggestionsDiv.innerHTML = `<div class="${className}">${escapeHtml(message)}</div>`;
            suggestionsDiv.classList.add('is-open');
        }

        function renderPrediction(result) {
            if (!result.found) {
                resultSlot.innerHTML = `
                    <div class="result-callout error" role="alert">
                        <span class="result-kicker">No match</span>
                        <p>${escapeHtml(result.message)}</p>
                    </div>
                `;
                return;
            }

            resultSlot.innerHTML = `
                <div class="result-callout">
                    <span class="result-kicker">Model result</span>
                    <p class="result-message">${escapeHtml(result.message)}</p>
                    <div class="salary-grid">
                        <div>
                            <span>Predicted</span>
                            <strong>$${escapeHtml(result.predicted_salary)}</strong>
                        </div>
                        <div>
                            <span>Actual</span>
                            <strong>$${escapeHtml(result.actual_salary)}</strong>
                        </div>
                    </div>
                </div>
            `;
        }

        async function runPrediction() {
            const playerName = playerInput.value.trim();

            if (!playerName) {
                playerInput.focus();
                return;
            }

            closeSuggestions();
            setLoading(true);

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ player_name: playerName })
                });
                const result = await response.json();

                if (!response.ok && !result.message) {
                    throw new Error('Prediction request failed');
                }

                renderPrediction(result);
                window.history.replaceState({}, '', window.location.pathname);
            } catch (error) {
                renderPrediction({
                    found: false,
                    message: 'Prediction unavailable. Try again.',
                    predicted_salary: '0',
                    actual_salary: '0'
                });
            } finally {
                setLoading(false);
            }
        }

        function submitPlayer(name) {
            playerInput.value = name;
            closeSuggestions();
            runPrediction();
        }

        function renderSuggestions(suggestions) {
            suggestionsDiv.innerHTML = '';

            if (!suggestions || suggestions.length === 0) {
                renderStatus('No players found', 'no-results');
                return;
            }

            suggestions.slice(0, 8).forEach((name) => {
                const item = document.createElement('button');
                item.type = 'button';
                item.className = 'suggestion-item';
                item.textContent = name;
                item.addEventListener('click', () => submitPlayer(name));
                item.addEventListener('keydown', (event) => {
                    if (event.key === 'ArrowDown' && item.nextElementSibling) {
                        event.preventDefault();
                        item.nextElementSibling.focus();
                    } else if (event.key === 'ArrowUp') {
                        event.preventDefault();
                        if (item.previousElementSibling) {
                            item.previousElementSibling.focus();
                        } else {
                            playerInput.focus();
                        }
                    } else if (event.key === 'Escape') {
                        closeSuggestions();
                        playerInput.focus();
                    }
                });
                suggestionsDiv.appendChild(item);
            });

            suggestionsDiv.classList.add('is-open');
        }

        async function fetchSuggestions() {
            const query = playerInput.value.trim();

            if (query.length === 0) {
                closeSuggestions();
                return;
            }

            if (activeRequest) {
                activeRequest.abort();
            }

            activeRequest = new AbortController();
            renderStatus('Searching...', 'loading');

            try {
                const response = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`, {
                    headers: { Accept: 'application/json' },
                    signal: activeRequest.signal
                });

                if (!response.ok) {
                    throw new Error('Autocomplete request failed');
                }

                renderSuggestions(await response.json());
            } catch (error) {
                if (error.name !== 'AbortError') {
                    renderStatus('Search unavailable', 'error');
                }
            }
        }

        predictionForm.addEventListener('submit', (event) => {
            event.preventDefault();
            runPrediction();
        });
        playerInput.addEventListener('input', debounce(fetchSuggestions, 120));
        playerInput.addEventListener('focus', () => {
            if (playerInput.value.trim()) {
                fetchSuggestions();
            }
        });
        playerInput.addEventListener('keydown', (event) => {
            const firstSuggestion = suggestionsDiv.querySelector('.suggestion-item');

            if (event.key === 'ArrowDown' && firstSuggestion) {
                event.preventDefault();
                firstSuggestion.focus();
            } else if (event.key === 'Escape') {
                closeSuggestions();
            }
        });

        document.addEventListener('pointerdown', (event) => {
            if (!playerInput.contains(event.target) && !suggestionsDiv.contains(event.target)) {
                closeSuggestions();
            }
        });

        if (window.playerNotFound) {
            playerInput.classList.add('error');
            setTimeout(() => playerInput.classList.remove('error'), 3000);
        }

        if (window.clearResultOnRefresh) {
            window.history.replaceState({}, '', window.location.pathname);
        }
    }

    function applyDocument(nextDocument) {
        const nextHeader = nextDocument.querySelector('.site-header');
        const nextMain = nextDocument.querySelector('main');
        const currentHeader = document.querySelector('.site-header');
        const currentMain = document.querySelector('main');

        if (!nextHeader || !nextMain || !currentHeader || !currentMain) {
            return false;
        }

        document.title = nextDocument.title;
        document.body.className = nextDocument.body.className;
        currentHeader.replaceWith(nextHeader);
        currentMain.replaceWith(nextMain);
        window.scrollTo({ top: 0, behavior: 'instant' });
        window.playerNotFound = false;
        window.clearResultOnRefresh = false;
        initPredictor();
        return true;
    }

    async function navigateTo(url, pushState = true) {
        const response = await fetch(url, { headers: { 'X-Requested-With': 'fetch' } });
        if (!response.ok) {
            window.location.href = url;
            return;
        }

        const html = await response.text();
        const nextDocument = new DOMParser().parseFromString(html, 'text/html');
        const swap = () => {
            if (!applyDocument(nextDocument)) {
                window.location.href = url;
                return;
            }
            if (pushState) {
                window.history.pushState({}, '', url);
            }
        };

        if (document.startViewTransition) {
            document.startViewTransition(swap);
        } else {
            document.documentElement.classList.add('is-navigating');
            swap();
            window.setTimeout(() => {
                document.documentElement.classList.remove('is-navigating');
            }, 180);
        }
    }

    document.addEventListener('click', (event) => {
        const link = event.target.closest('a[href]');
        if (!link || link.target || link.hasAttribute('download')) {
            return;
        }

        const url = new URL(link.href);
        if (url.origin !== window.location.origin || !routes.has(url.pathname)) {
            return;
        }

        event.preventDefault();
        navigateTo(url.pathname);
    });

    window.addEventListener('popstate', () => {
        const path = routes.has(window.location.pathname) ? window.location.pathname : '/';
        navigateTo(path, false);
    });

    window.addEventListener('DOMContentLoaded', initPredictor);
})();
