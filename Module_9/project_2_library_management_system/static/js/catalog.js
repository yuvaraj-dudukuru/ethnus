// catalog.js — browse the catalog, borrow/return, and show my loans live.
const $ = (s) => document.querySelector(s);
let debounce;

async function loadBooks() {
  const q = encodeURIComponent($("#search").value.trim());
  let url = `/api/books/?search=${q}`;
  if ($("#only-available").checked) url += "&available=true";
  const { data } = await api(url);
  const books = data.results || data;
  const wrap = $("#books");
  if (!books.length) { wrap.innerHTML = '<p class="empty">No books found.</p>'; return; }
  wrap.innerHTML = books.map((b) => `
    <div class="card">
      <h3>${b.title}</h3>
      <p class="muted">${b.author ? b.author.name : ""} · ${b.isbn}</p>
      <p><span class="badge ${b.available ? "ok" : "bad"}">${b.copies_available}/${b.copies_total} available</span></p>
      ${window.LOGGED_IN ? `
        <div class="row-actions">
          <button class="btn ok small" ${b.available ? "" : "disabled"} data-issue="${b.id}">Borrow</button>
          <button class="btn small" data-return="${b.id}">Return</button>
        </div>` : ""}
    </div>`).join("");
  wrap.querySelectorAll("[data-issue]").forEach((btn) =>
    btn.addEventListener("click", () => act(btn.dataset.issue, "issue")));
  wrap.querySelectorAll("[data-return]").forEach((btn) =>
    btn.addEventListener("click", () => act(btn.dataset.return, "return")));
}

async function act(bookId, kind) {
  const { ok, data } = await api(`/api/books/${bookId}/${kind}/`, "POST");
  if (!ok) alert(data && data.detail ? data.detail : "Action failed.");
  await loadBooks();
  await loadLoans();
}

async function loadLoans() {
  if (!window.LOGGED_IN) return;
  const { data } = await api("/api/issues/");
  const loans = (data.results || data).filter((i) => !i.returned);
  const tbody = $("#loans");
  if (!tbody) return;
  tbody.innerHTML = loans.length ? loans.map((i) => `
    <tr>
      <td>${i.book_title}</td><td>${i.due_date}</td>
      <td><span class="badge ${i.is_overdue ? "bad" : "ok"}">${i.is_overdue ? "overdue" : "on time"}</span></td>
      <td>${i.fine}</td>
    </tr>`).join("") : '<tr><td colspan="4" class="empty">No active loans.</td></tr>';
}

$("#search").addEventListener("input", () => {
  clearTimeout(debounce); debounce = setTimeout(loadBooks, 250);
});
$("#only-available").addEventListener("change", loadBooks);

(async function init() { await loadBooks(); await loadLoans(); })();
