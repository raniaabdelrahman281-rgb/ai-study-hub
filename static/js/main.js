document.addEventListener('DOMContentLoaded', function () {
    // Mobile nav toggle (old top-navbar, kept for logged-out pages)
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });
    }

    // Mobile sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    // Live search for notes (JS-driven, hits a small JSON endpoint - no DRF)
    const searchInput = document.getElementById('note-live-search');
    const searchResults = document.getElementById('search-results');
    if (searchInput && searchResults) {
        let debounceTimer;
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            if (query.length < 2) {
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
                return;
            }
            debounceTimer = setTimeout(() => {
                fetch(`/notes/search-api/?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        searchResults.innerHTML = '';
                        if (data.results.length === 0) {
                            searchResults.innerHTML = '<div style="padding:10px 14px;">No notes found.</div>';
                        } else {
                            data.results.forEach(note => {
                                const a = document.createElement('a');
                                a.href = note.url;
                                a.innerHTML = `<strong>${note.title}</strong><br><small>${note.snippet}</small>`;
                                searchResults.appendChild(a);
                            });
                        }
                        searchResults.style.display = 'block';
                    })
                    .catch(() => { searchResults.style.display = 'none'; });
            }, 250);
        });

        document.addEventListener('click', function (e) {
            if (!searchResults.contains(e.target) && e.target !== searchInput) {
                searchResults.style.display = 'none';
            }
        });
    }

    // Client-side filtering for simple lists (data-filter-target items)
    const filterInput = document.querySelector('[data-live-filter]');
    if (filterInput) {
        const targetSelector = filterInput.getAttribute('data-live-filter');
        filterInput.addEventListener('input', function () {
            const term = this.value.toLowerCase();
            document.querySelectorAll(targetSelector).forEach(el => {
                const text = el.textContent.toLowerCase();
                el.style.display = text.includes(term) ? '' : 'none';
            });
        });
    }

    // Task "mark complete" toggle via fetch (AJAX, no page reload)
    document.querySelectorAll('.task-toggle-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.dataset.url;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                },
            })
                .then(res => res.json())
                .then(data => {
                    const row = this.closest('.item-row');
                    if (row) {
                        row.classList.toggle('completed', data.is_completed);
                        this.textContent = data.is_completed ? '↩️ Undo' : '✅ Complete';
                    }
                });
        });
    });
});
