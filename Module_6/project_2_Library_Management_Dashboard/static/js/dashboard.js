/* ============================================================================
 *  dashboard.js — ALL of the Module 6 front-end logic for the LIBRARY.
 * ----------------------------------------------------------------------------
 *  The page never reloads. JavaScript uses fetch() to talk to the Module-5 REST
 *  API in the background (AJAX) and updates the screen in place.
 *
 *  ⭐ THE STAR FEATURE of this project is the BOOKS multi-filter bar.
 *     Three separate inputs — a search box, an author dropdown and an
 *     availability dropdown — are all stored in ONE small "state" object.
 *     Whenever any of them changes, we (after a short debounce pause) build a
 *     single query string from that object and make ONE request, e.g.:
 *
 *         GET /api/books/?search=harry&author=2&available=true&page=1
 *
 *  Other things this file does:
 *     - Issue a book   -> POST /api/books/{id}/issue/      (an M5 @action)
 *     - Return a book  -> POST /api/issues/{id}/return_book/ (an M5 @action)
 *       …and live-updates the affected row's status badge.
 *     - Lists loans and members (staff only).
 *     - Token login (admin / admin) so write actions are allowed.
 *
 *  Open DevTools → Network tab to watch every request.
 * ==========================================================================*/

document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------------
    //  CONFIG, ELEMENTS & SMALL HELPERS
    // ------------------------------------------------------------------
    const API = '/api';
    const PAGE_SIZE = 10;   // matches StandardPagination on the server

    // Grab the elements we use, once.
    const el = {
        // auth
        loginForm:   document.getElementById('login-form'),
        loginUser:   document.getElementById('login-username'),
        loginPass:   document.getElementById('login-password'),
        loggedInBar: document.getElementById('logged-in-bar'),
        currentUser: document.getElementById('current-user'),
        logoutBtn:   document.getElementById('logout-btn'),
        flash:       document.getElementById('flash'),
        // books filter bar
        fSearch:     document.getElementById('f-search'),
        fAuthor:     document.getElementById('f-author'),
        fAvailable:  document.getElementById('f-available'),
        fClear:      document.getElementById('f-clear'),
        // books table + states
        booksRows:     document.getElementById('books-rows'),
        booksSpinner:  document.getElementById('books-spinner'),
        booksEmpty:    document.getElementById('books-empty'),
        booksError:    document.getElementById('books-error'),
        booksPrev:     document.getElementById('books-prev'),
        booksNext:     document.getElementById('books-next'),
        booksPageInfo: document.getElementById('books-pageinfo'),
        // loans
        loansLocked:  document.getElementById('loans-locked'),
        loansContent: document.getElementById('loans-content'),
        loansSpinner: document.getElementById('loans-spinner'),
        loansEmpty:   document.getElementById('loans-empty'),
        loansRows:    document.getElementById('loans-rows'),
        // members
        membersLocked:  document.getElementById('members-locked'),
        membersContent: document.getElementById('members-content'),
        membersSpinner: document.getElementById('members-spinner'),
        membersRows:    document.getElementById('members-rows'),
        // issue modal
        issueModalEl: document.getElementById('issue-modal'),
        issueForm:    document.getElementById('issue-form'),
        issueTitle:   document.getElementById('issue-book-title'),
        issueMember:  document.getElementById('issue-member'),
        issueDue:     document.getElementById('issue-due'),
    };

    // The Bootstrap modal controller for the "Issue book" pop-up.
    const issueModal = new bootstrap.Modal(el.issueModalEl);

    // Show/hide using Bootstrap's d-none (display:none) class.
    const show = n => n.classList.remove('d-none');
    const hide = n => n.classList.add('d-none');

    // Coloured auto-hiding message at the top. type = 'success' | 'danger' | 'info'.
    let flashTimer = null;
    function showFlash(message, type) {
        el.flash.textContent = message;
        el.flash.className = 'alert alert-' + (type || 'info');
        clearTimeout(flashTimer);
        flashTimer = setTimeout(() => hide(el.flash), 4000);
    }

    // Escape user text before putting it into HTML (prevents broken markup).
    function esc(text) {
        const d = document.createElement('div');
        d.textContent = text == null ? '' : text;
        return d.innerHTML;
    }

    // ------------------------------------------------------------------
    //  LOGIN / TOKEN
    // ------------------------------------------------------------------
    const TOKEN_KEY = 'lib_token';
    const USER_KEY  = 'lib_user';
    const getToken = () => localStorage.getItem(TOKEN_KEY);
    const getUser  = () => localStorage.getItem(USER_KEY);

    // Build request headers; attach the login token if we have one.
    function headers() {
        const h = { 'Content-Type': 'application/json' };
        const t = getToken();
        if (t) h['Authorization'] = 'Token ' + t;
        return h;
    }

    // Update everything that depends on being logged in or not.
    function refreshAuthUI() {
        const loggedIn = !!getToken();
        if (loggedIn) {
            hide(el.loginForm);
            show(el.loggedInBar);
            el.loggedInBar.classList.add('d-flex');
            el.currentUser.textContent = getUser() || 'user';
            // Unlock the staff-only tabs.
            hide(el.loansLocked);   show(el.loansContent);
            hide(el.membersLocked); show(el.membersContent);
            // Load the members list (also fills the issue modal dropdown).
            loadMembers();
        } else {
            show(el.loginForm);
            hide(el.loggedInBar);
            el.loggedInBar.classList.remove('d-flex');
            // Lock the staff-only tabs again.
            show(el.loansLocked);   hide(el.loansContent);
            show(el.membersLocked); hide(el.membersContent);
        }
    }

    el.loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const username = el.loginUser.value.trim();
        const password = el.loginPass.value;
        try {
            const res = await fetch(API + '/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (!res.ok) {
                showFlash('Login failed — check your username and password.', 'danger');
                return;
            }
            const data = await res.json();           // { token: "..." }
            localStorage.setItem(TOKEN_KEY, data.token);
            localStorage.setItem(USER_KEY, username);
            el.loginPass.value = '';
            refreshAuthUI();
            showFlash('Logged in. You can now issue and return books.', 'success');
        } catch (err) {
            showFlash('Could not reach the server to log in.', 'danger');
        }
    });

    el.logoutBtn.addEventListener('click', function () {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        refreshAuthUI();
        showFlash('Logged out.', 'info');
    });

    // ==================================================================
    //  BOOKS  (the multi-filter feature)
    // ==================================================================

    // ⭐ THE STATE OBJECT. These few values fully describe what the books
    //    table should currently show. Every filter input writes into here,
    //    and buildBooksURL() reads from here. One source of truth.
    const filters = {
        search: '',       // text typed in the search box
        author: '',       // selected author id ('' = all)
        available: '',    // '', 'true' or 'false'
        page: 1,          // current page number
        count: 0,         // total books the API reports (for pagination)
    };

    // Turn the state object into a single /api/books/ URL. We only add a
    // parameter if it actually has a value, keeping the URL tidy.
    function buildBooksURL() {
        const p = new URLSearchParams();
        if (filters.search)    p.set('search', filters.search);
        if (filters.author)    p.set('author', filters.author);
        if (filters.available) p.set('available', filters.available);
        p.set('page', filters.page);
        return API + '/books/?' + p.toString();
    }

    // Fill the author dropdown from /api/authors/ (added in Module 6).
    async function loadAuthors() {
        try {
            const res = await fetch(API + '/authors/');
            if (!res.ok) return;
            const data = await res.json();
            const list = data.results || data;
            list.forEach(a => {
                const opt = document.createElement('option');
                opt.value = a.id;
                opt.textContent = a.name;
                el.fAuthor.appendChild(opt);
            });
        } catch (err) {
            console.error('Could not load authors', err);
        }
    }

    // Fetch one page of books (with the current filters) and draw them.
    async function loadBooks() {
        hide(el.booksEmpty); hide(el.booksError);
        show(el.booksSpinner);
        el.booksRows.innerHTML = '';
        try {
            const res = await fetch(buildBooksURL(), { headers: headers() });
            hide(el.booksSpinner);
            if (!res.ok) { show(el.booksError); updateBooksPagination(); return; }

            const data = await res.json();   // { count, next, previous, results }
            filters.count = data.count;
            if (!data.results.length) {
                show(el.booksEmpty);
            } else {
                data.results.forEach(addBookRow);
            }
            updateBooksPagination();
        } catch (err) {
            hide(el.booksSpinner);
            show(el.booksError);
            console.error(err);
        }
    }

    // Build ONE book row. The status badge and Issue button depend on stock.
    function addBookRow(book) {
        const tr = document.createElement('tr');
        tr.dataset.id = book.id;

        // Green "Available" badge vs red "Out of stock" badge.
        const badge = book.is_available
            ? `<span class="badge bg-success">Available</span>`
            : `<span class="badge bg-danger">Out of stock</span>`;

        // The Issue button is disabled when no copies are free.
        const issueBtn = book.is_available
            ? `<button class="btn btn-sm btn-outline-success issue-btn"
                       data-id="${book.id}" data-title="${esc(book.title)}">Issue</button>`
            : `<button class="btn btn-sm btn-outline-secondary" disabled>Issue</button>`;

        tr.innerHTML = `
            <td>${esc(book.title)}</td>
            <td>${esc(book.author_name)}</td>
            <td><code>${esc(book.isbn)}</code></td>
            <td>${book.copies_available} / ${book.copies_total}</td>
            <td class="status-cell">${badge}</td>
            <td>${issueBtn}</td>
        `;
        el.booksRows.appendChild(tr);
    }

    function updateBooksPagination() {
        const totalPages = Math.max(1, Math.ceil(filters.count / PAGE_SIZE));
        el.booksPageInfo.textContent =
            `Page ${filters.page} of ${totalPages}  (${filters.count} books)`;
        el.booksPrev.disabled = filters.page <= 1;
        el.booksNext.disabled = filters.page >= totalPages;
    }

    el.booksPrev.addEventListener('click', () => {
        if (filters.page > 1) { filters.page--; loadBooks(); }
    });
    el.booksNext.addEventListener('click', () => {
        filters.page++; loadBooks();
    });

    // ---- Debounce: wait until the user stops interacting for 300ms ----
    function debounce(fn, delay) {
        let timer = null;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    // Read ALL THREE filter inputs into the state object, reset to page 1,
    // and reload. This single function is wired to every filter input below.
    const applyFilters = debounce(function () {
        filters.search    = el.fSearch.value.trim();
        filters.author    = el.fAuthor.value;
        filters.available = el.fAvailable.value;
        filters.page      = 1;     // any filter change starts at page 1
        loadBooks();
    }, 300);

    // The search box changes as you type; the dropdowns change on selection.
    el.fSearch.addEventListener('input', applyFilters);
    el.fAuthor.addEventListener('change', applyFilters);
    el.fAvailable.addEventListener('change', applyFilters);

    // "Clear" resets every input and the state, then reloads.
    el.fClear.addEventListener('click', function () {
        el.fSearch.value = '';
        el.fAuthor.value = '';
        el.fAvailable.value = '';
        applyFilters();
    });

    // ==================================================================
    //  ISSUE A BOOK  (open the modal, then POST the @action)
    // ==================================================================

    // Clicking an "Issue" button (event delegation on the books table).
    el.booksRows.addEventListener('click', function (e) {
        if (!e.target.classList.contains('issue-btn')) return;
        if (!getToken()) {
            showFlash('Please log in as staff (admin / admin) to issue books.', 'danger');
            return;
        }
        // Remember which book we are issuing and show its title in the modal.
        el.issueForm.dataset.bookId = e.target.dataset.id;
        el.issueTitle.textContent = e.target.dataset.title;
        // Default due date = two weeks from today (handy starting value).
        const d = new Date();
        d.setDate(d.getDate() + 14);
        el.issueDue.value = d.toISOString().slice(0, 10);   // YYYY-MM-DD
        issueModal.show();
    });

    // Submitting the modal form actually issues the book.
    el.issueForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const bookId = el.issueForm.dataset.bookId;
        const payload = {
            member: Number(el.issueMember.value),
            due_date: el.issueDue.value,
        };
        try {
            const res = await fetch(`${API}/books/${bookId}/issue/`, {
                method: 'POST',
                headers: headers(),
                body: JSON.stringify(payload),
            });
            if (res.status === 201) {
                issueModal.hide();
                showFlash('Book issued. A copy was taken off the shelf.', 'success');
                loadBooks();                 // refresh stock + status badge
                if (getToken()) loadLoans();  // keep the Loans tab in sync
            } else {
                // e.g. {"detail": "No copies available."} or validation errors.
                const err = await res.json();
                showFlash('Could not issue: ' + formatErrors(err), 'danger');
            }
        } catch (err) {
            showFlash('Could not reach the server to issue the book.', 'danger');
        }
    });

    // Turn an API error object into one readable sentence.
    function formatErrors(errObj) {
        if (errObj && errObj.detail) return errObj.detail;
        try {
            return Object.entries(errObj)
                .map(([f, m]) => `${f}: ${Array.isArray(m) ? m.join(' ') : m}`)
                .join(' | ');
        } catch (e) { return 'please check the values and try again.'; }
    }

    // ==================================================================
    //  LOANS (issues) — list + RETURN action.  Staff only.
    // ==================================================================
    async function loadLoans() {
        if (!getToken()) return;             // locked when logged out
        hide(el.loansEmpty);
        show(el.loansSpinner);
        el.loansRows.innerHTML = '';
        try {
            const res = await fetch(API + '/issues/', { headers: headers() });
            hide(el.loansSpinner);
            if (!res.ok) return;
            const data = await res.json();
            const list = data.results || data;
            if (!list.length) { show(el.loansEmpty); return; }
            list.forEach(addLoanRow);
        } catch (err) {
            hide(el.loansSpinner);
            console.error(err);
        }
    }

    function addLoanRow(issue) {
        const tr = document.createElement('tr');
        tr.dataset.id = issue.id;

        // Work out a status badge: Returned / Overdue / On loan.
        const today = new Date().toISOString().slice(0, 10);
        let badge;
        if (issue.returned) {
            badge = `<span class="badge bg-secondary">Returned</span>`;
        } else if (issue.due_date < today) {
            badge = `<span class="badge bg-danger">Overdue</span>`;
        } else {
            badge = `<span class="badge bg-primary">On loan</span>`;
        }

        // Return button only makes sense while the book is still out.
        const returnBtn = issue.returned
            ? `<button class="btn btn-sm btn-outline-secondary" disabled>Return</button>`
            : `<button class="btn btn-sm btn-outline-warning return-btn"
                       data-id="${issue.id}">Return</button>`;

        tr.innerHTML = `
            <td>${esc(issue.book_title)}</td>
            <td>${esc(issue.member_name)}</td>
            <td>${esc(issue.due_date)}</td>
            <td class="status-cell">${badge}</td>
            <td>${issue.fine > 0 ? '₹' + issue.fine : '—'}</td>
            <td>${returnBtn}</td>
        `;
        el.loansRows.appendChild(tr);
    }

    // Clicking "Return" (event delegation on the loans table).
    el.loansRows.addEventListener('click', async function (e) {
        if (!e.target.classList.contains('return-btn')) return;
        const id = e.target.dataset.id;
        try {
            const res = await fetch(`${API}/issues/${id}/return_book/`, {
                method: 'POST',
                headers: headers(),
            });
            if (res.ok) {
                showFlash('Book returned. A copy is back on the shelf.', 'success');
                loadLoans();   // refresh the loan's status badge
                loadBooks();   // the book's stock + badge changed too
            } else {
                const err = await res.json();
                showFlash('Could not return: ' + formatErrors(err), 'danger');
            }
        } catch (err) {
            showFlash('Could not reach the server to return the book.', 'danger');
        }
    });

    // ==================================================================
    //  MEMBERS — list + fill the issue-modal dropdown.  Staff only.
    // ==================================================================
    async function loadMembers() {
        if (!getToken()) return;
        show(el.membersSpinner);
        el.membersRows.innerHTML = '';
        try {
            const res = await fetch(API + '/members/', { headers: headers() });
            hide(el.membersSpinner);
            if (!res.ok) return;
            const data = await res.json();
            const list = data.results || data;

            // 1) Fill the Members table.
            list.forEach(m => {
                const tr = document.createElement('tr');
                tr.innerHTML =
                    `<td>${esc(m.name)}</td><td>${esc(m.email)}</td><td>${esc(m.join_date)}</td>`;
                el.membersRows.appendChild(tr);
            });

            // 2) Fill the "Issue book" modal's member dropdown.
            el.issueMember.innerHTML = '<option value="">Choose a member…</option>';
            list.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m.id;
                opt.textContent = m.name + ' (' + m.email + ')';
                el.issueMember.appendChild(opt);
            });
        } catch (err) {
            hide(el.membersSpinner);
            console.error(err);
        }
    }

    // ------------------------------------------------------------------
    //  TAB EVENTS — (re)load data when a staff tab is opened
    // ------------------------------------------------------------------
    document.getElementById('loans-tab')
        .addEventListener('shown.bs.tab', loadLoans);
    document.getElementById('members-tab')
        .addEventListener('shown.bs.tab', loadMembers);

    // ------------------------------------------------------------------
    //  START EVERYTHING
    // ------------------------------------------------------------------
    refreshAuthUI();   // show the right login state (+ load members if logged in)
    loadAuthors();     // fill the author filter dropdown
    loadBooks();       // load page 1 of books (public — no login needed)
});
