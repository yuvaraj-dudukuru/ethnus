// events.js — event cards with seats-left, register/cancel, "my events".
const $ = (s) => document.querySelector(s);
let debounce;

async function loadEvents() {
  const q = encodeURIComponent($("#search").value.trim());
  let url = `/api/events/?search=${q}`;
  if ($("#upcoming").checked) url += "&upcoming=true";
  const { data } = await api(url);
  const events = data.results || data;
  $("#events").innerHTML = events.length ? events.map((e) => `
    <div class="card">
      <h3>${e.title}</h3>
      <p class="muted">${new Date(e.datetime).toLocaleString()}${e.venue ? " · " + e.venue.name : ""}</p>
      <p>${e.description || ""}</p>
      <p>${Number(e.price) > 0 ? `<span class="price">$${e.price}</span>` : '<span class="badge ok">Free</span>'}
        · <span class="badge ${e.seats_left > 0 ? "ok" : "bad"}">${e.seats_left} / ${e.capacity} seats left</span></p>
      ${buttons(e)}
    </div>`).join("") : '<p class="empty">No events found.</p>';
  wire();
}

function buttons(e) {
  if (!window.LOGGED_IN) return '<a class="btn small" href="/login/">Log in to register</a>';
  let html = `<button class="btn primary small" ${e.seats_left > 0 ? "" : "disabled"} data-reg="${e.id}">Register</button>
              <button class="btn small" data-cancel="${e.id}">Cancel</button>`;
  if (e.organizer === window.USERNAME) {
    html += ` <button class="btn small" data-att="${e.id}">View attendees</button>
              <div data-attlist="${e.id}"></div>`;
  }
  return html;
}

function wire() {
  document.querySelectorAll("[data-reg]").forEach((b) =>
    b.addEventListener("click", () => act(b.dataset.reg, "register")));
  document.querySelectorAll("[data-cancel]").forEach((b) =>
    b.addEventListener("click", () => act(b.dataset.cancel, "cancel")));
  document.querySelectorAll("[data-att]").forEach((b) =>
    b.addEventListener("click", () => attendees(b.dataset.att)));
}

async function act(id, kind) {
  const { ok, data } = await api(`/api/events/${id}/${kind}/`, "POST");
  if (!ok) alert(data.detail || "Failed.");
  await loadEvents();
  await loadMine();
}

async function attendees(id) {
  const box = document.querySelector(`[data-attlist="${id}"]`);
  const { ok, data } = await api(`/api/events/${id}/attendees/`);
  if (!ok) { box.innerHTML = '<p class="muted">Not allowed.</p>'; return; }
  box.innerHTML = data.length
    ? "<ul>" + data.map((r) => `<li>${r.user}</li>`).join("") + "</ul>"
    : '<p class="empty">No attendees yet.</p>';
}

async function loadMine() {
  if (!window.LOGGED_IN) return;
  const { data } = await api("/api/registrations/");
  const regs = data.results || data;
  const tbody = $("#mine");
  if (!tbody) return;
  tbody.innerHTML = regs.length ? regs.map((r) => `
    <tr><td>${r.event_title}</td>
    <td><span class="badge ${r.status === "CONFIRMED" ? "ok" : "muted"}">${r.status}</span></td></tr>`).join("")
    : '<tr><td colspan="2" class="empty">No registrations.</td></tr>';
}

$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadEvents, 250); });
$("#upcoming").addEventListener("change", loadEvents);

(async function init() { await loadEvents(); await loadMine(); })();
