/* ============================================================================
 *  dashboard.js — ALL of the Module 6 front-end logic for the INVENTORY.
 * ----------------------------------------------------------------------------
 *  The page never reloads. JavaScript uses fetch() to talk to the Module-5 REST
 *  API in the background (AJAX) and keeps the stock table up to date.
 *
 *  ⭐ THE STAR FEATURE: "real-time-ish" updates by POLLING + DIFFING.
 *     Every 10 seconds we re-fetch the product list and COMPARE the new numbers
 *     with what is already shown:
 *       - if a product's STOCK changed, its cell briefly FLASHES
 *         (green when it went up, red when it went down),
 *       - rows at/below the LOW_STOCK threshold AUTO-HIGHLIGHT as "Low".
 *     This is the simple way to feel live without extra server software. For
 *     TRUE instant push you would use WebSockets via Django Channels — the
 *     server would push a message the moment stock changes, instead of the
 *     browser asking again and again. Polling is easier and needs no new infra.
 *
 *  It also does full product CRUD (admin only), just like Project 1.
 *
 *  NOTE ON PAGINATION: the products API uses CURSOR pagination (next/previous
 *  links, no page numbers). To show and diff the WHOLE inventory we simply
 *  follow the "next" links until there are none left.
 *
 *  Open DevTools → Network tab to watch the requests repeat every 10 seconds.
 * ==========================================================================*/

document.addEventListener('DOMContentLoaded', function () {

    const API = '/api';

    // Products at or below this many units are flagged "Low". Change it freely.
    const LOW_STOCK = 25;

    // How often (milliseconds) to poll the server when auto-refresh is on.
    const POLL_MS = 10000;   // 10 seconds

    // Grab the elements once.
    const el = {
        loginForm:   document.getElementById('login-form'),
        loginUser:   document.getElementById('login-username'),
        loginPass:   document.getElementById('login-password'),
        loggedInBar: document.getElementById('logged-in-bar'),
        currentUser: document.getElementById('current-user'),
        logoutBtn:   document.getElementById('logout-btn'),
        flash:       document.getElementById('flash'),
        search:      document.getElementById('search'),
        autoToggle:  document.getElementById('auto-toggle'),
        liveDot:     document.getElementById('live-dot'),
        refreshBtn:  document.getElementById('refresh-btn'),
        addBtn:      document.getElementById('add-btn'),
        lastUpdated: document.getElementById('last-updated'),
        lowLabel:    document.getElementById('low-threshold-label'),
        spinner:     document.getElementById('spinner'),
        emptyState:  document.getElementById('empty-state'),
        errorState:  document.getElementById('error-state'),
        rows:        document.getElementById('rows'),
        // modal
        modalEl:     document.getElementById('product-modal'),
        modalTitle:  document.getElementById('product-modal-title'),
        form:        document.getElementById('product-form'),
        pName:       document.getElementById('p-name'),
        pCategory:   document.getElementById('p-category'),
        pPrice:      document.getElementById('p-price'),
        pStock:      document.getElementById('p-stock'),
        pDescription:document.getElementById('p-description'),
    };
    el.lowLabel.textContent = LOW_STOCK;

    const productModal = new bootstrap.Modal(el.modalEl);

    // State we remember between polls.
    let me = { is_authenticated: false, is_staff: false };
    let pollTimer = null;
    let firstLoad = true;
    // The stock we currently SHOW for each product id — used to detect changes.
    const shownStock = new Map();
    // The full product object for each id — used to prefill the Edit modal.
    const productMap = new Map();

    // ------------------------------------------------------------------
    //  HELPERS
    // ------------------------------------------------------------------
    const show = n => n.classList.remove('d-none');
    const hide = n => n.classList.add('d-none');

    let flashTimer = null;
    function showFlash(message, type) {
        el.flash.textContent = message;
        el.flash.className = 'alert alert-' + (type || 'info');
        clearTimeout(flashTimer);
        flashTimer = setTimeout(() => hide(el.flash), 4000);
    }

    function esc(text) {
        const d = document.createElement('div');
        d.textContent = text == null ? '' : text;
        return d.innerHTML;
    }

    // ------------------------------------------------------------------
    //  AUTH (token + /api/me/)
    // ------------------------------------------------------------------
    const TOKEN_KEY = 'inv_token';
    const getToken = () => localStorage.getItem(TOKEN_KEY);
    function headers() {
        const h = { 'Content-Type': 'application/json' };
        const t = getToken();
        if (t) h['Authorization'] = 'Token ' + t;
        return h;
    }

    async function checkMe() {
        try {
            const res = await fetch(API + '/me/', { headers: headers() });
            me = await res.json();
        } catch (e) { me = { is_authenticated: false, is_staff: false }; }
        refreshAuthUI();
    }

    function refreshAuthUI() {
        if (me.is_authenticated) {
            hide(el.loginForm); show(el.loggedInBar);
            el.loggedInBar.classList.add('d-flex');
            el.currentUser.textContent = me.username + (me.is_staff ? ' (admin)' : '');
        } else {
            show(el.loginForm); hide(el.loggedInBar);
            el.loggedInBar.classList.remove('d-flex');
        }
        // The "Add product" button is for admins only.
        if (me.is_staff) show(el.addBtn); else hide(el.addBtn);
    }

    el.loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        try {
            const res = await fetch(API + '/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: el.loginUser.value.trim(),
                    password: el.loginPass.value,
                }),
            });
            if (!res.ok) { showFlash('Login failed — check your username and password.', 'danger'); return; }
            const data = await res.json();
            localStorage.setItem(TOKEN_KEY, data.token);
            el.loginPass.value = '';
            await checkMe();
            rebuildTable();          // redraw rows so admin Edit/Delete appear
            showFlash('Logged in.' + (me.is_staff ? ' You can manage products.' : ''), 'success');
        } catch (err) { showFlash('Could not reach the server to log in.', 'danger'); }
    });

    el.logoutBtn.addEventListener('click', function () {
        localStorage.removeItem(TOKEN_KEY);
        me = { is_authenticated: false, is_staff: false };
        refreshAuthUI();
        rebuildTable();
        showFlash('Logged out.', 'info');
    });

    // Clear the table and force a full rebuild (used when auth changes).
    function rebuildTable() {
        el.rows.innerHTML = '';
        shownStock.clear();
        productMap.clear();
        refresh();
    }

    // ------------------------------------------------------------------
    //  CATEGORIES (for the modal dropdown)
    // ------------------------------------------------------------------
    async function loadCategories() {
        try {
            const res = await fetch(API + '/categories/');
            if (!res.ok) return;
            const data = await res.json();
            const list = data.results || data;   // we disabled pagination here
            el.pCategory.length = 1;
            list.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id; opt.textContent = c.name;
                el.pCategory.appendChild(opt);
            });
        } catch (e) { console.error('Could not load categories', e); }
    }

    // ------------------------------------------------------------------
    //  FETCH ALL PRODUCTS (follow the cursor "next" links)
    // ------------------------------------------------------------------
    async function fetchAllProducts() {
        const params = new URLSearchParams();
        const term = el.search.value.trim();
        if (term) params.set('search', term);
        let url = API + '/products/?' + params.toString();

        const all = [];
        let safety = 50;   // never loop forever, even on a huge catalog
        while (url && safety-- > 0) {
            const res = await fetch(url, { headers: headers() });
            if (!res.ok) throw new Error('Bad response ' + res.status);
            const data = await res.json();
            (data.results || []).forEach(p => all.push(p));
            url = data.next;   // CursorPagination gives the next page's full URL
        }
        return all;
    }

    // ------------------------------------------------------------------
    //  REFRESH + DIFF  (the heart of the live updates)
    // ------------------------------------------------------------------
    async function refresh() {
        if (firstLoad) { hide(el.emptyState); hide(el.errorState); show(el.spinner); }
        try {
            const products = await fetchAllProducts();
            hide(el.spinner); hide(el.errorState);

            if (!products.length) {
                el.rows.innerHTML = '';
                shownStock.clear(); productMap.clear();
                show(el.emptyState);
            } else {
                hide(el.emptyState);
                diffIntoTable(products);
            }
            el.lastUpdated.textContent = new Date().toLocaleTimeString();
        } catch (err) {
            hide(el.spinner);
            if (firstLoad) show(el.errorState);   // only shout on first load
            console.error(err);
        }
        firstLoad = false;
    }

    // Compare the freshly fetched products to what is on screen and update only
    // what changed. This is the "diffing" muscle.
    function diffIntoTable(products) {
        const seen = new Set();

        products.forEach(p => {
            seen.add(p.id);
            productMap.set(p.id, p);
            let row = el.rows.querySelector(`tr[data-id="${p.id}"]`);

            if (!row) {
                // Brand-new row: create it (no flash on first appearance).
                row = document.createElement('tr');
                row.dataset.id = p.id;
                el.rows.appendChild(row);
                renderRow(row, p, /*flash=*/null);
                shownStock.set(p.id, p.stock);
                return;
            }

            // Existing row: did the stock change since we last showed it?
            const prev = shownStock.get(p.id);
            let flash = null;
            if (prev !== undefined && prev !== p.stock) {
                flash = p.stock > prev ? 'flash-up' : 'flash-down';
            }
            renderRow(row, p, flash);
            shownStock.set(p.id, p.stock);
        });

        // Remove rows for products that no longer exist (e.g. deleted).
        el.rows.querySelectorAll('tr[data-id]').forEach(row => {
            const id = Number(row.dataset.id);
            if (!seen.has(id)) {
                row.remove();
                shownStock.delete(id);
                productMap.delete(id);
            }
        });
    }

    // Fill (or refill) one row's cells. If 'flash' is set, animate the stock cell.
    function renderRow(row, p, flash) {
        // Low-stock auto-highlight on the whole row.
        row.classList.toggle('table-warning', p.stock > 0 && p.stock <= LOW_STOCK);
        row.classList.toggle('table-danger', p.stock === 0);

        // Status badge.
        let badge;
        if (p.stock === 0)              badge = '<span class="badge bg-danger">Out of stock</span>';
        else if (p.stock <= LOW_STOCK)  badge = '<span class="badge bg-warning text-dark">Low</span>';
        else                            badge = '<span class="badge bg-success">In stock</span>';

        // Admin-only action buttons.
        const actions = me.is_staff
            ? `<button class="btn btn-sm btn-outline-primary edit-btn" data-id="${p.id}">Edit</button>
               <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${p.id}">Delete</button>`
            : '<span class="text-muted">—</span>';

        row.innerHTML = `
            <td>${esc(p.name)}</td>
            <td>${esc(p.category_name)}</td>
            <td class="text-end">₹${esc(p.price)}</td>
            <td class="text-end fw-bold stock-cell">${p.stock}</td>
            <td>${badge}</td>
            <td>${actions}</td>
        `;

        // Trigger the flash by adding the animation class to the stock cell.
        if (flash) {
            const cell = row.querySelector('.stock-cell');
            cell.classList.remove('flash-up', 'flash-down');
            void cell.offsetWidth;          // restart the CSS animation
            cell.classList.add(flash);
        }
    }

    // ------------------------------------------------------------------
    //  POLLING CONTROL
    // ------------------------------------------------------------------
    function startPolling() {
        stopPolling();
        pollTimer = setInterval(refresh, POLL_MS);   // ⭐ the periodic refresh
        el.liveDot.style.visibility = 'visible';
    }
    function stopPolling() {
        if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
        el.liveDot.style.visibility = 'hidden';
    }

    el.autoToggle.addEventListener('change', function () {
        if (el.autoToggle.checked) { startPolling(); refresh(); }
        else { stopPolling(); }
    });

    el.refreshBtn.addEventListener('click', refresh);

    // ------------------------------------------------------------------
    //  SEARCH (debounced)
    // ------------------------------------------------------------------
    function debounce(fn, delay) {
        let t = null;
        return function (...a) { clearTimeout(t); t = setTimeout(() => fn.apply(this, a), delay); };
    }
    el.search.addEventListener('input', debounce(refresh, 300));

    // ------------------------------------------------------------------
    //  ADD / EDIT PRODUCT (admin)
    // ------------------------------------------------------------------
    el.addBtn.addEventListener('click', function () {
        el.form.reset();
        delete el.form.dataset.editId;          // "add" mode
        el.modalTitle.textContent = 'Add product';
        productModal.show();
    });

    // Edit + Delete buttons (event delegation on the table body).
    el.rows.addEventListener('click', async function (e) {
        const editBtn = e.target.closest('.edit-btn');
        const delBtn  = e.target.closest('.delete-btn');

        if (editBtn) {
            const p = productMap.get(Number(editBtn.dataset.id));
            if (!p) return;
            el.form.dataset.editId = p.id;       // "edit" mode
            el.modalTitle.textContent = 'Edit product';
            el.pName.value = p.name;
            el.pCategory.value = p.category;
            el.pPrice.value = p.price;
            el.pStock.value = p.stock;
            el.pDescription.value = p.description || '';
            productModal.show();
        }

        if (delBtn) {
            const p = productMap.get(Number(delBtn.dataset.id));
            if (!p) return;
            if (!confirm(`Delete "${p.name}"? This cannot be undone.`)) return;
            try {
                const res = await fetch(`${API}/products/${p.id}/`, {
                    method: 'DELETE', headers: headers(),
                });
                if (res.status === 204) { showFlash('Product deleted.', 'success'); refresh(); }
                else if (res.status === 403) showFlash('Only an admin may delete products.', 'danger');
                else showFlash('Could not delete (status ' + res.status + ').', 'danger');
            } catch (err) { showFlash('Could not reach the server to delete.', 'danger'); }
        }
    });

    // Saving the modal form: POST to create, PATCH to update.
    el.form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const editId = el.form.dataset.editId;
        const payload = {
            name: el.pName.value.trim(),
            category: Number(el.pCategory.value),
            price: el.pPrice.value,
            stock: Number(el.pStock.value),
            description: el.pDescription.value.trim(),
        };
        const url = editId ? `${API}/products/${editId}/` : `${API}/products/`;
        const method = editId ? 'PATCH' : 'POST';
        try {
            const res = await fetch(url, { method, headers: headers(), body: JSON.stringify(payload) });
            if (res.ok) {
                productModal.hide();
                showFlash(editId ? 'Product updated.' : 'Product added.', 'success');
                refresh();
            } else {
                const err = await res.json();
                showFlash('Could not save: ' + JSON.stringify(err), 'danger');
            }
        } catch (err) { showFlash('Could not reach the server to save.', 'danger'); }
    });

    // ------------------------------------------------------------------
    //  START EVERYTHING
    // ------------------------------------------------------------------
    checkMe();           // figure out if we are an admin (shows/hides buttons)
    loadCategories();    // fill the modal dropdown
    refresh();           // first load of the inventory
    startPolling();      // begin the 10-second auto-refresh
});
