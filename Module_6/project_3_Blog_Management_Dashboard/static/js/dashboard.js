/* ============================================================================
 *  dashboard.js — ALL of the Module 6 front-end logic for the BLOG.
 * ----------------------------------------------------------------------------
 *  The page never reloads. JavaScript uses fetch() to talk to the Module-5 REST
 *  API in the background (AJAX) and updates the screen in place.
 *
 *  Three things to learn here:
 *    1) POST CARDS — we take the array of posts the API returns and MAP each one
 *       to a card (cloned from a <template>), with every piece of user text
 *       safely ESCAPED so it can never break the page or inject markup.
 *    2) COMMENTS PER POST — each card loads its own comments from
 *       /api/posts/{slug}/comments/ and appends them, and new comments are
 *       added to the list without any page reload.
 *    3) OPTIMISTIC LIKES ⭐ — clicking the heart updates the number INSTANTLY,
 *       then sends the POST in the background, and ROLLS BACK if it fails. This
 *       is the pattern that makes apps feel instant.
 *
 *  Buttons that change data are AUTH-GATED: we ask /api/me/ whether the visitor
 *  is logged in, and only then show the comment box / write form / enable likes.
 *
 *  Open DevTools → Network tab to watch every request.
 * ==========================================================================*/

document.addEventListener('DOMContentLoaded', function () {

    const API = '/api';
    const PAGE_SIZE = 10;   // matches StandardPagination on the server

    // Grab the elements we use once.
    const el = {
        loginForm:   document.getElementById('login-form'),
        loginUser:   document.getElementById('login-username'),
        loginPass:   document.getElementById('login-password'),
        loggedInBar: document.getElementById('logged-in-bar'),
        currentUser: document.getElementById('current-user'),
        logoutBtn:   document.getElementById('logout-btn'),
        flash:       document.getElementById('flash'),
        writeCard:   document.getElementById('write-card'),
        writeForm:   document.getElementById('write-form'),
        wTitle:      document.getElementById('w-title'),
        wCategory:   document.getElementById('w-category'),
        wPublish:    document.getElementById('w-publish'),
        wBody:       document.getElementById('w-body'),
        search:      document.getElementById('search'),
        spinner:     document.getElementById('spinner'),
        emptyState:  document.getElementById('empty-state'),
        errorState:  document.getElementById('error-state'),
        feed:        document.getElementById('feed'),
        prevBtn:     document.getElementById('prev-btn'),
        nextBtn:     document.getElementById('next-btn'),
        pageInfo:    document.getElementById('page-info'),
        cardTemplate: document.getElementById('card-template'),
    };

    // The few facts we remember between requests.
    const state = { page: 1, search: '', count: 0 };

    // "me" describes the current visitor. Filled by checkMe() (calls /api/me/).
    let me = { is_authenticated: false, username: null };

    // ------------------------------------------------------------------
    //  SMALL HELPERS
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

    // Escape user text before putting it into HTML (prevents broken/injected markup).
    function esc(text) {
        const d = document.createElement('div');
        d.textContent = text == null ? '' : text;
        return d.innerHTML;
    }

    // Turn an ISO timestamp into a short friendly date like "25 Jun 2026".
    function niceDate(iso) {
        try { return new Date(iso).toLocaleDateString(undefined,
            { day: 'numeric', month: 'short', year: 'numeric' }); }
        catch (e) { return iso; }
    }

    // ------------------------------------------------------------------
    //  LOGIN / TOKEN / "WHO AM I?"
    // ------------------------------------------------------------------
    const TOKEN_KEY = 'blog_token';
    const getToken = () => localStorage.getItem(TOKEN_KEY);

    function headers() {
        const h = { 'Content-Type': 'application/json' };
        const t = getToken();
        if (t) h['Authorization'] = 'Token ' + t;
        return h;
    }

    // Ask the API who we are. This is the AUTH GATE: the answer decides which
    // buttons appear. An anonymous visitor gets {is_authenticated:false}.
    async function checkMe() {
        try {
            const res = await fetch(API + '/me/', { headers: headers() });
            me = await res.json();
        } catch (err) {
            me = { is_authenticated: false };
        }
        refreshAuthUI();
    }

    // Show/hide the login bar and the write-post form based on "me".
    function refreshAuthUI() {
        if (me.is_authenticated) {
            hide(el.loginForm);
            show(el.loggedInBar);
            el.loggedInBar.classList.add('d-flex');
            el.currentUser.textContent = me.username;
            show(el.writeCard);
        } else {
            show(el.loginForm);
            hide(el.loggedInBar);
            el.loggedInBar.classList.remove('d-flex');
            hide(el.writeCard);
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
            const data = await res.json();
            localStorage.setItem(TOKEN_KEY, data.token);
            el.loginPass.value = '';
            await checkMe();            // re-check who we are now
            loadCategories();           // the write form's dropdown
            loadPosts();                // redraw feed (comment boxes appear)
            showFlash('Logged in. You can now like, comment and write posts.', 'success');
        } catch (err) {
            showFlash('Could not reach the server to log in.', 'danger');
        }
    });

    el.logoutBtn.addEventListener('click', async function () {
        localStorage.removeItem(TOKEN_KEY);
        me = { is_authenticated: false };
        refreshAuthUI();
        loadPosts();
        showFlash('Logged out.', 'info');
    });

    // ------------------------------------------------------------------
    //  CATEGORIES (for the write-post dropdown)
    // ------------------------------------------------------------------
    async function loadCategories() {
        try {
            const res = await fetch(API + '/categories/');
            if (!res.ok) return;
            const data = await res.json();
            const list = data.results || data;
            // Keep the first "(no category)" option, then add the real ones.
            el.wCategory.length = 1;
            list.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name;
                el.wCategory.appendChild(opt);
            });
        } catch (err) { console.error('Could not load categories', err); }
    }

    // ------------------------------------------------------------------
    //  LOAD + RENDER POSTS  (the card feed)
    // ------------------------------------------------------------------
    function buildPostsURL() {
        const p = new URLSearchParams();
        if (state.search) p.set('search', state.search);
        p.set('page', state.page);
        return API + '/posts/?' + p.toString();
    }

    async function loadPosts() {
        hide(el.emptyState); hide(el.errorState);
        show(el.spinner);
        el.feed.innerHTML = '';
        try {
            const res = await fetch(buildPostsURL(), { headers: headers() });
            hide(el.spinner);
            if (!res.ok) { show(el.errorState); updatePagination(); return; }
            const data = await res.json();   // { count, next, previous, results }
            state.count = data.count;
            if (!data.results.length) {
                show(el.emptyState);
            } else {
                // MAP each post object to a card and add it to the feed.
                data.results.forEach(post => el.feed.appendChild(buildCard(post)));
            }
            updatePagination();
        } catch (err) {
            hide(el.spinner);
            show(el.errorState);
            console.error(err);
        }
    }

    // Build ONE card for a post by cloning the <template> and filling it in.
    function buildCard(post) {
        const node = el.cardTemplate.content.cloneNode(true);
        const card = node.querySelector('.post-card');
        card.dataset.slug = post.slug;

        // Title + meta line (author • category • date). All text is escaped.
        card.querySelector('.js-title').textContent = post.title;
        const cat = post.category_name ? ' • ' + post.category_name : '';
        card.querySelector('.js-meta').textContent =
            `by ${post.author_name}${cat} • ${niceDate(post.created)}`;

        // --- LIKES ---
        const likeBtn   = card.querySelector('.js-like');
        const likeCount = card.querySelector('.js-like-count');
        likeCount.textContent = post.likes;
        likeBtn.addEventListener('click', () => likePost(post.slug, likeBtn, likeCount));

        // --- COMMENTS toggle ---
        const commentsBox  = card.querySelector('.js-comments');
        const commentList  = card.querySelector('.js-comment-list');
        const commentForm  = card.querySelector('.js-comment-form');
        const commentInput = card.querySelector('.js-comment-input');
        const toggleBtn    = card.querySelector('.js-toggle-comments');

        toggleBtn.addEventListener('click', async () => {
            // First click: fetch the comments. Later clicks: just show/hide.
            if (commentsBox.classList.contains('d-none')) {
                show(commentsBox);
                if (!commentsBox.dataset.loaded) {
                    await loadComments(post.slug, commentList);
                    commentsBox.dataset.loaded = '1';
                }
                // Only logged-in users get the comment box (auth gate).
                if (me.is_authenticated) show(commentForm); else hide(commentForm);
            } else {
                hide(commentsBox);
            }
        });

        // Submitting the comment form posts a new comment.
        commentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await addComment(post.slug, commentInput, commentList);
        });

        return node;
    }

    function updatePagination() {
        const totalPages = Math.max(1, Math.ceil(state.count / PAGE_SIZE));
        el.pageInfo.textContent =
            `Page ${state.page} of ${totalPages}  (${state.count} posts)`;
        el.prevBtn.disabled = state.page <= 1;
        el.nextBtn.disabled = state.page >= totalPages;
    }

    el.prevBtn.addEventListener('click', () => {
        if (state.page > 1) { state.page--; loadPosts(); }
    });
    el.nextBtn.addEventListener('click', () => { state.page++; loadPosts(); });

    // ------------------------------------------------------------------
    //  ⭐ OPTIMISTIC LIKE
    // ------------------------------------------------------------------
    async function likePost(slug, btn, countSpan) {
        if (!me.is_authenticated) {
            showFlash('Please log in to like posts.', 'danger');
            return;
        }
        // 1) OPTIMISTIC UPDATE: change the screen IMMEDIATELY, before the server
        //    has even answered. The app feels instant.
        const previous = Number(countSpan.textContent);
        countSpan.textContent = previous + 1;
        btn.firstChild.textContent = '❤️ ';   // swap white heart -> red heart
        btn.classList.add('liked');

        // 2) Send the real request in the background.
        try {
            const res = await fetch(`${API}/posts/${slug}/like/`, {
                method: 'POST',
                headers: headers(),
            });
            if (res.ok) {
                // 3a) Success: trust the server's authoritative count.
                const data = await res.json();
                countSpan.textContent = data.likes;
            } else {
                throw new Error('Server rejected the like');
            }
        } catch (err) {
            // 3b) FAILURE: ROLL BACK the optimistic change.
            countSpan.textContent = previous;
            btn.firstChild.textContent = '🤍 ';
            btn.classList.remove('liked');
            showFlash('Could not save your like — please try again.', 'danger');
        }
    }

    // ------------------------------------------------------------------
    //  COMMENTS — load per post + add new without reload
    // ------------------------------------------------------------------
    async function loadComments(slug, listEl) {
        listEl.innerHTML = '<div class="text-muted">Loading comments…</div>';
        try {
            const res = await fetch(`${API}/posts/${slug}/comments/`, { headers: headers() });
            if (!res.ok) { listEl.innerHTML = '<div class="text-danger">Could not load comments.</div>'; return; }
            const data = await res.json();
            const list = data.results || data;
            listEl.innerHTML = '';
            if (!list.length) {
                listEl.innerHTML = '<div class="text-muted">No comments yet. Be the first!</div>';
            } else {
                list.forEach(c => listEl.appendChild(renderComment(c)));
            }
        } catch (err) {
            listEl.innerHTML = '<div class="text-danger">Could not load comments.</div>';
        }
    }

    // Build one comment line (escaped).
    function renderComment(c) {
        const div = document.createElement('div');
        div.className = 'mb-1';
        div.innerHTML =
            `<strong>${esc(c.user_name)}</strong>: ${esc(c.body)} ` +
            `<span class="text-muted">· ${niceDate(c.created)}</span>`;
        return div;
    }

    async function addComment(slug, inputEl, listEl) {
        const body = inputEl.value.trim();
        if (!body) return;
        try {
            const res = await fetch(`${API}/posts/${slug}/comments/`, {
                method: 'POST',
                headers: headers(),
                body: JSON.stringify({ body }),
            });
            if (res.status === 201) {
                const newComment = await res.json();
                // Remove a "No comments yet" placeholder if present.
                if (listEl.querySelector('.text-muted')) listEl.innerHTML = '';
                listEl.appendChild(renderComment(newComment));   // append, no reload
                inputEl.value = '';
            } else {
                const err = await res.json();
                showFlash('Could not comment: ' + JSON.stringify(err), 'danger');
            }
        } catch (err) {
            showFlash('Could not reach the server to comment.', 'danger');
        }
    }

    // ------------------------------------------------------------------
    //  WRITE A NEW POST
    // ------------------------------------------------------------------
    el.writeForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const payload = {
            title: el.wTitle.value.trim(),
            body: el.wBody.value.trim(),
            status: el.wPublish.checked ? 'P' : 'D',   // Published or Draft
        };
        // Only include a category if one was chosen.
        if (el.wCategory.value) payload.category = Number(el.wCategory.value);

        try {
            const res = await fetch(API + '/posts/', {
                method: 'POST',
                headers: headers(),
                body: JSON.stringify(payload),
            });
            if (res.status === 201) {
                el.writeForm.reset();
                el.wPublish.checked = true;
                if (payload.status === 'P') {
                    showFlash('Post published!', 'success');
                    state.page = 1; state.search = ''; el.search.value = '';
                    loadPosts();
                } else {
                    showFlash('Saved as a draft (drafts are hidden from the public feed).', 'info');
                }
            } else {
                const err = await res.json();
                showFlash('Could not save post: ' + JSON.stringify(err), 'danger');
            }
        } catch (err) {
            showFlash('Could not reach the server to save the post.', 'danger');
        }
    });

    // ------------------------------------------------------------------
    //  SEARCH (debounced)
    // ------------------------------------------------------------------
    function debounce(fn, delay) {
        let timer = null;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }
    el.search.addEventListener('input', debounce(function () {
        state.search = el.search.value.trim();
        state.page = 1;
        loadPosts();
    }, 300));

    // ------------------------------------------------------------------
    //  START EVERYTHING
    // ------------------------------------------------------------------
    checkMe();          // ask /api/me/ who we are, then show the right buttons
    loadCategories();   // fill the write-post category dropdown
    loadPosts();        // load page 1 of the feed (public — no login needed)
});
