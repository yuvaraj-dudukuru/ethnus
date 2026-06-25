/* ============================================================================
 *  dashboard.js — ALL of the Module 6 front-end logic lives here.
 * ----------------------------------------------------------------------------
 *  This file makes the static dashboard.html page come alive. It NEVER reloads
 *  the page. Instead it uses fetch() to send small background (AJAX) requests
 *  to the REST API from Module 5, and then updates the HTML in place.
 *
 *  What it does, in the order a student should learn it:
 *     1) On page load, fetch the student list and the department list.
 *     2) Render the students into the table.
 *     3) Live search (debounced) as you type.
 *     4) Intercept the "Add student" form and POST it as JSON.
 *     5) Delete a student (event delegation on the table).
 *     6) Inline-edit a student's marks with a PATCH request.
 *     7) Pagination (Previous / Next) using the API's paged response.
 *     8) Show spinner / flash / empty / error states at the right moments.
 *
 *  Reading the list is public. Adding / editing / deleting needs you to be
 *  logged in — so this file also handles a tiny token-based login.
 *
 *  Open your browser DevTools → Network tab to SEE every request this makes.
 * ==========================================================================*/

// Wait until the whole HTML page is parsed before we touch any elements.
// (The <script> tag is at the bottom of the page, but this is the safe habit.)
document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------------
    //  CONFIG & SMALL HELPERS
    // ------------------------------------------------------------------

    // The base address of our API. Because the page is served by the same
    // Django server, we can use a relative path — no domain needed.
    const API = '/api';

    // How many students the API returns per page (matches StandardPagination
    // in the Django settings). We use it to work out "Page X of Y".
    const PAGE_SIZE = 10;

    // Grab the page elements once, so we don't keep searching the DOM.
    const el = {
        // Login / auth
        loginForm:    document.getElementById('login-form'),
        loginUser:    document.getElementById('login-username'),
        loginPass:    document.getElementById('login-password'),
        loggedInBar:  document.getElementById('logged-in-bar'),
        currentUser:  document.getElementById('current-user'),
        logoutBtn:    document.getElementById('logout-btn'),
        // Add form
        addForm:      document.getElementById('add-form'),
        addRoll:      document.getElementById('add-roll'),
        addName:      document.getElementById('add-name'),
        addEmail:     document.getElementById('add-email'),
        addMarks:     document.getElementById('add-marks'),
        addDept:      document.getElementById('add-department'),
        // Search + table
        search:       document.getElementById('search'),
        rows:         document.getElementById('student-rows'),
        // Status placeholders
        spinner:      document.getElementById('spinner'),
        emptyState:   document.getElementById('empty-state'),
        errorState:   document.getElementById('error-state'),
        flash:        document.getElementById('flash'),
        // Pagination
        prevBtn:      document.getElementById('prev-btn'),
        nextBtn:      document.getElementById('next-btn'),
        pageInfo:     document.getElementById('page-info'),
    };

    // "State" = the few facts we need to remember between requests.
    const state = {
        page: 1,        // which page of students we are looking at
        search: '',     // the current search text
        count: 0,       // total number of students the API reports
    };

    // The keys we use to remember the login token in the browser's
    // localStorage (so a page refresh keeps you logged in).
    const TOKEN_KEY = 'smd_token';
    const USER_KEY  = 'smd_user';

    // Read whatever token/username we saved earlier (may be null).
    function getToken() { return localStorage.getItem(TOKEN_KEY); }
    function getUser()  { return localStorage.getItem(USER_KEY); }

    // Build the headers for a request. We always send JSON; if we have a
    // login token we also attach it so the API knows who we are.
    function headers() {
        const h = { 'Content-Type': 'application/json' };
        const t = getToken();
        if (t) h['Authorization'] = 'Token ' + t;
        return h;
    }

    // ------------------------------------------------------------------
    //  UI STATE HELPERS (spinner / flash / empty / error)
    // ------------------------------------------------------------------

    // Show or hide an element using Bootstrap's "d-none" (display:none) class.
    function show(node) { node.classList.remove('d-none'); }
    function hide(node) { node.classList.add('d-none'); }

    // Show a coloured message at the top. type is 'success' or 'danger'.
    // It disappears on its own after a few seconds.
    let flashTimer = null;
    function showFlash(message, type) {
        el.flash.textContent = message;
        // Reset the colour classes, then apply the one we want.
        el.flash.className = 'alert alert-' + (type || 'info');
        clearTimeout(flashTimer);
        flashTimer = setTimeout(() => hide(el.flash), 4000);
    }

    // Hide the three status placeholders (we show the right one when needed).
    function clearStates() {
        hide(el.spinner);
        hide(el.emptyState);
        hide(el.errorState);
    }

    // ------------------------------------------------------------------
    //  LOGIN / LOGOUT
    // ------------------------------------------------------------------

    // Update the login bar to match whether we currently have a token.
    function refreshAuthUI() {
        if (getToken()) {
            hide(el.loginForm);
            show(el.loggedInBar);
            el.loggedInBar.classList.add('d-flex');   // make it a flex row
            el.currentUser.textContent = getUser() || 'user';
        } else {
            show(el.loginForm);
            hide(el.loggedInBar);
            el.loggedInBar.classList.remove('d-flex');
        }
    }

    // Handle the login form: ask the API for a token in exchange for the
    // username + password. The endpoint is POST /api/login/.
    el.loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();   // stop the browser from reloading the page
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
            const data = await res.json();          // { "token": "abc123..." }
            localStorage.setItem(TOKEN_KEY, data.token);
            localStorage.setItem(USER_KEY, username);
            el.loginPass.value = '';
            refreshAuthUI();
            showFlash('Logged in. You can now add, edit and delete students.', 'success');
        } catch (err) {
            showFlash('Could not reach the server to log in.', 'danger');
        }
    });

    // Logout simply forgets the token we stored. (The API also has a
    // /api/logout/ endpoint that deletes the token server-side; for this
    // teaching app, forgetting it in the browser is enough.)
    el.logoutBtn.addEventListener('click', function () {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        refreshAuthUI();
        showFlash('Logged out.', 'info');
    });

    // ------------------------------------------------------------------
    //  LOAD DEPARTMENTS (to fill the "Add student" dropdown)
    // ------------------------------------------------------------------
    async function loadDepartments() {
        try {
            const res = await fetch(API + '/departments/');
            if (!res.ok) return;
            const data = await res.json();
            // Departments are also paginated; the list is in data.results.
            const list = data.results || data;
            list.forEach(dept => {
                const opt = document.createElement('option');
                opt.value = dept.id;
                opt.textContent = dept.name;
                el.addDept.appendChild(opt);
            });
        } catch (err) {
            // Not fatal — the page still works, the dropdown is just empty.
            console.error('Could not load departments', err);
        }
    }

    // ------------------------------------------------------------------
    //  LOAD + RENDER STUDENTS  (the heart of the page)
    // ------------------------------------------------------------------

    // Build the API URL for the current page + search text.
    function buildListURL() {
        const params = new URLSearchParams();
        params.set('page', state.page);
        if (state.search) params.set('search', state.search);
        return API + '/students/?' + params.toString();
    }

    // Fetch one page of students and show them.
    async function loadStudents() {
        clearStates();
        show(el.spinner);          // show "Loading…" while we wait
        el.rows.innerHTML = '';    // clear the old rows

        try {
            const res = await fetch(buildListURL(), { headers: headers() });
            hide(el.spinner);

            if (!res.ok) {            // e.g. 500 server error
                show(el.errorState);
                updatePagination();
                return;
            }

            // The API returns a "page envelope":
            //   { count, next, previous, results: [ ...students ] }
            const data = await res.json();
            state.count = data.count;

            if (!data.results.length) {
                show(el.emptyState);          // nothing matched
            } else {
                data.results.forEach(addRowToTable);
            }
            updatePagination();
        } catch (err) {
            // fetch() only throws for network-level problems (server down).
            hide(el.spinner);
            show(el.errorState);
            console.error(err);
        }
    }

    // Create ONE table row for a student object and append it to the table.
    function addRowToTable(student) {
        const tr = document.createElement('tr');
        tr.dataset.id = student.id;   // remember the id on the row for later

        // Department may be a nested object {id, name, strength}.
        const deptName = student.department ? student.department.name : '—';

        // We build the row's HTML. The marks cell holds a small number input
        // and a "Save" button so marks can be edited inline (see PATCH below).
        tr.innerHTML = `
            <td>${student.roll}</td>
            <td>${escapeHtml(student.name)}</td>
            <td>${escapeHtml(student.email)}</td>
            <td>${escapeHtml(deptName)}</td>
            <td>
                <div class="input-group input-group-sm">
                    <input type="number" class="form-control marks-input"
                           value="${student.marks}" min="0" style="max-width:70px">
                    <button class="btn btn-outline-primary save-marks-btn"
                            title="Save marks">💾</button>
                </div>
            </td>
            <td>
                <button class="btn btn-sm btn-outline-danger delete-btn"
                        title="Delete student">🗑</button>
            </td>
        `;
        el.rows.appendChild(tr);
    }

    // Tiny helper: stop user-supplied text (names/emails) from breaking the
    // HTML or injecting markup. Always escape data before putting it in HTML.
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text == null ? '' : text;
        return div.innerHTML;
    }

    // ------------------------------------------------------------------
    //  PAGINATION
    // ------------------------------------------------------------------
    function updatePagination() {
        const totalPages = Math.max(1, Math.ceil(state.count / PAGE_SIZE));
        el.pageInfo.textContent =
            `Page ${state.page} of ${totalPages}  (${state.count} students)`;
        // Disable "Previous" on the first page, "Next" on the last page.
        el.prevBtn.disabled = state.page <= 1;
        el.nextBtn.disabled = state.page >= totalPages;
    }

    el.prevBtn.addEventListener('click', function () {
        if (state.page > 1) { state.page--; loadStudents(); }
    });
    el.nextBtn.addEventListener('click', function () {
        state.page++; loadStudents();
    });

    // ------------------------------------------------------------------
    //  LIVE SEARCH (debounced)
    // ------------------------------------------------------------------
    //  "Debounce" = wait until the user STOPS typing for 300ms before sending
    //  a request. Without it, typing "asha" would fire 4 separate requests.
    function debounce(fn, delay) {
        let timer = null;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    el.search.addEventListener('input', debounce(function () {
        state.search = el.search.value.trim();
        state.page = 1;          // every new search starts on page 1
        loadStudents();
    }, 300));

    // ------------------------------------------------------------------
    //  ADD A STUDENT  (intercept the form, POST as JSON)
    // ------------------------------------------------------------------
    el.addForm.addEventListener('submit', async function (e) {
        e.preventDefault();      // do NOT let the browser submit/reload

        if (!getToken()) {
            showFlash('Please log in first (admin / admin) to add a student.', 'danger');
            return;
        }

        // Collect the form values into the JSON shape the API expects.
        // Note: the API wants "department_id" (a number), not the whole object.
        const payload = {
            roll: Number(el.addRoll.value),
            name: el.addName.value.trim(),
            email: el.addEmail.value.trim(),
            marks: Number(el.addMarks.value),
            department_id: Number(el.addDept.value),
        };

        try {
            const res = await fetch(API + '/students/', {
                method: 'POST',
                headers: headers(),
                body: JSON.stringify(payload),
            });

            if (res.status === 201) {            // 201 = Created
                el.addForm.reset();
                showFlash(`Added student "${payload.name}".`, 'success');
                state.page = 1;
                state.search = '';
                el.search.value = '';
                loadStudents();
            } else {
                // The API sends back a JSON object explaining what was wrong,
                // e.g. {"email": ["Official @college.edu email required."]}.
                const err = await res.json();
                showFlash('Could not add: ' + formatErrors(err), 'danger');
            }
        } catch (err) {
            showFlash('Could not reach the server to add the student.', 'danger');
        }
    });

    // Turn the API's error object into one readable sentence.
    function formatErrors(errObj) {
        try {
            return Object.entries(errObj)
                .map(([field, msgs]) =>
                    `${field}: ${Array.isArray(msgs) ? msgs.join(' ') : msgs}`)
                .join(' | ');
        } catch (e) {
            return 'please check the values and try again.';
        }
    }

    // ------------------------------------------------------------------
    //  DELETE + INLINE EDIT  (event delegation on the table body)
    // ------------------------------------------------------------------
    //  Instead of adding a click handler to every button (rows come and go),
    //  we add ONE handler to the table body and check what was clicked. This
    //  is called "event delegation" and is the standard pattern for lists.
    el.rows.addEventListener('click', async function (e) {
        const row = e.target.closest('tr');
        if (!row) return;
        const id = row.dataset.id;

        // ---- DELETE button ----
        if (e.target.classList.contains('delete-btn')) {
            if (!getToken()) {
                showFlash('Please log in as admin to delete.', 'danger');
                return;
            }
            if (!confirm('Delete this student? This cannot be undone.')) return;

            try {
                const res = await fetch(`${API}/students/${id}/`, {
                    method: 'DELETE',
                    headers: headers(),
                });
                if (res.status === 204) {        // 204 = deleted, no content
                    showFlash('Student deleted.', 'success');
                    loadStudents();              // refresh the current page
                } else if (res.status === 403) {
                    showFlash('Only the admin user may delete students.', 'danger');
                } else {
                    showFlash('Could not delete (status ' + res.status + ').', 'danger');
                }
            } catch (err) {
                showFlash('Could not reach the server to delete.', 'danger');
            }
        }

        // ---- SAVE MARKS button (inline PATCH) ----
        if (e.target.classList.contains('save-marks-btn')) {
            if (!getToken()) {
                showFlash('Please log in to edit marks.', 'danger');
                return;
            }
            const input = row.querySelector('.marks-input');
            const newMarks = Number(input.value);

            try {
                // PATCH updates ONLY the fields we send (here, just "marks").
                const res = await fetch(`${API}/students/${id}/`, {
                    method: 'PATCH',
                    headers: headers(),
                    body: JSON.stringify({ marks: newMarks }),
                });
                if (res.ok) {
                    showFlash('Marks updated.', 'success');
                    input.classList.add('is-valid');     // brief green tick
                    setTimeout(() => input.classList.remove('is-valid'), 1500);
                } else {
                    const err = await res.json();
                    showFlash('Could not update marks: ' + formatErrors(err), 'danger');
                }
            } catch (err) {
                showFlash('Could not reach the server to update marks.', 'danger');
            }
        }
    });

    // ------------------------------------------------------------------
    //  START EVERYTHING
    // ------------------------------------------------------------------
    refreshAuthUI();      // show the right login state
    loadDepartments();    // fill the dropdown
    loadStudents();       // load page 1 of the students
});
