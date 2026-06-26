// clinic.js — doctor directory, booking, and "my appointments".
const $ = (s) => document.querySelector(s);
let debounce;

async function loadDepartments() {
  const { data } = await api("/api/departments/");
  (data.results || data).forEach((d) =>
    $("#dept").insertAdjacentHTML("beforeend", `<option value="${d.id}">${d.name}</option>`));
}

async function loadDoctors() {
  const q = encodeURIComponent($("#search").value.trim());
  let url = `/api/doctors/?search=${q}`;
  if ($("#dept").value) url += `&department=${$("#dept").value}`;
  const { data } = await api(url);
  const docs = data.results || data;
  const wrap = $("#doctors");
  wrap.innerHTML = docs.length ? docs.map((d) => `
    <div class="card">
      <h3>Dr. ${d.name}</h3>
      <p class="muted">${d.specialization || ""} · ${d.department ? d.department.name : ""}</p>
      ${window.LOGGED_IN ? `
        <label>Date & time<input type="datetime-local" data-when="${d.id}"></label>
        <input placeholder="Reason" data-reason="${d.id}">
        <button class="btn primary small" data-book="${d.id}">Book</button>
        <span class="msg muted" data-msg="${d.id}"></span>` : ""}
    </div>`).join("") : '<p class="empty">No doctors found.</p>';
  wrap.querySelectorAll("[data-book]").forEach((b) =>
    b.addEventListener("click", () => book(b.dataset.book)));
}

async function book(id) {
  const when = document.querySelector(`[data-when="${id}"]`).value;
  const reason = document.querySelector(`[data-reason="${id}"]`).value;
  const msg = document.querySelector(`[data-msg="${id}"]`);
  if (!when) { msg.textContent = "Pick a date & time."; return; }
  const { ok, data } = await api(`/api/doctors/${id}/book/`, "POST",
    { datetime: new Date(when).toISOString(), reason });
  msg.textContent = ok ? "Booked!" : (data.detail || "Failed.");
  if (ok) loadAppointments();
}

async function loadAppointments() {
  if (!window.LOGGED_IN) return;
  const { data } = await api("/api/appointments/");
  const appts = data.results || data;
  const tbody = $("#appts");
  if (!tbody) return;
  tbody.innerHTML = appts.length ? appts.map((a) => `
    <tr>
      <td>Dr. ${a.doctor_name}</td>
      <td>${new Date(a.datetime).toLocaleString()}</td>
      <td><span class="badge ${a.status === "CANCELLED" ? "bad" : "ok"}">${a.status}</span></td>
      <td>${a.status === "BOOKED" ? `<button class="btn bad small" data-cancel="${a.id}">Cancel</button>` : ""}</td>
    </tr>`).join("") : '<tr><td colspan="4" class="empty">No appointments.</td></tr>';
  tbody.querySelectorAll("[data-cancel]").forEach((b) =>
    b.addEventListener("click", async () => {
      await api(`/api/appointments/${b.dataset.cancel}/cancel/`, "POST");
      loadAppointments();
    }));
}

$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadDoctors, 250); });
$("#dept").addEventListener("change", loadDoctors);

(async function init() { await loadDepartments(); await loadDoctors(); await loadAppointments(); })();
