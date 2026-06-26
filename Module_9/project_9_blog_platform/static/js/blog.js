// blog.js — post feed, optimistic likes, comments, markdown preview + drafts.
const $ = (s) => document.querySelector(s);
let debounce;

// Tiny markdown: bold, italic, inline code, links, line breaks. (Demo-grade.)
function md(text) {
  return (text || "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/\*(.+?)\*/g, "<i>$1</i>")
    .replace(/`(.+?)`/g, "<code>$1</code>")
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
    .replace(/\n/g, "<br>");
}

async function loadPosts() {
  const q = encodeURIComponent($("#search").value.trim());
  const { data } = await api(`/api/posts/?search=${q}`);
  const posts = data.results || data;
  $("#posts").innerHTML = posts.length ? posts.map((p) => `
    <div class="card">
      <h3>${p.title} ${p.status === "DRAFT" ? '<span class="badge muted">draft</span>' : ""}</h3>
      <p class="muted">by ${p.author}${p.category ? " · " + p.category.name : ""}</p>
      <div>${md(p.body)}</div>
      <div class="toolbar" style="margin-top:10px">
        <button class="btn small ${p.liked_by_me ? "bad" : ""}" data-like="${p.slug}">
          ♥ <span class="lc">${p.like_count}</span></button>
        <button class="btn small" data-comments="${p.id}">💬 ${p.comment_count}</button>
      </div>
      <div class="comments" data-clist="${p.id}" style="display:none"></div>
    </div>`).join("") : '<p class="empty">No posts yet.</p>';
  wire();
}

function wire() {
  document.querySelectorAll("[data-like]").forEach((b) =>
    b.addEventListener("click", () => toggleLike(b)));
  document.querySelectorAll("[data-comments]").forEach((b) =>
    b.addEventListener("click", () => toggleComments(b.dataset.comments)));
}

async function toggleLike(btn) {
  if (!window.LOGGED_IN) { location.href = "/login/"; return; }
  const span = btn.querySelector(".lc");
  // Optimistic UI: flip immediately, then reconcile with the server.
  const wasLiked = btn.classList.contains("bad");
  btn.classList.toggle("bad");
  span.textContent = Number(span.textContent) + (wasLiked ? -1 : 1);
  const { ok, data } = await api(`/api/posts/${btn.dataset.like}/like/`, "POST");
  if (ok) { span.textContent = data.like_count; btn.classList.toggle("bad", data.liked); }
}

async function toggleComments(postId) {
  const box = document.querySelector(`[data-clist="${postId}"]`);
  if (box.style.display === "block") { box.style.display = "none"; return; }
  box.style.display = "block";
  const { data } = await api(`/api/comments/?post=${postId}`);
  const comments = data.results || data;
  box.innerHTML = comments.map((c) =>
    `<p><b>${c.user}:</b> ${c.body}</p>`).join("") || '<p class="muted">No comments.</p>';
  if (window.LOGGED_IN) {
    box.insertAdjacentHTML("beforeend", `
      <form data-cform="${postId}"><input name="body" placeholder="Add a comment…" required>
      <button class="btn small primary">Post</button></form>`);
    box.querySelector("form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = e.target.body.value;
      const { ok } = await api("/api/comments/", "POST", { post: Number(postId), body });
      if (ok) { e.target.reset(); toggleComments(postId); toggleComments(postId); }
    });
  }
}

function wireNewPost() {
  const form = $("#new-post");
  if (!form) return;
  $("#body").addEventListener("input", (e) => { $("#preview").innerHTML = md(e.target.value); });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(form).entries());
    const { ok, data } = await api("/api/posts/", "POST", body);
    $("#post-msg").textContent = ok ? "Saved!" : JSON.stringify(data);
    if (ok) { form.reset(); $("#preview").innerHTML = ""; loadPosts(); }
  });
}

$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadPosts, 250); });
(function init() { loadPosts(); wireNewPost(); })();
