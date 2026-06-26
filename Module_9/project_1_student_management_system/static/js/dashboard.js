// dashboard.js — talks to the DRF API to render the student dashboard.
// Uses the window.api() helper from base.html (adds CSRF + JSON automatically).

const $ = (sel) => document.querySelector(sel);
let debounce;

// Load departments into the filter + the add-form select, and the stats box.
async function loadDepartments() {
  const { data } = await api("/api/departments/");
  const depts = data.results || data;
  const filter = $("#dept-filter");
  const addSel = $("#add-dept");
  depts.forEach((d) => {
    filter.insertAdjacentHTML("beforeend", `<option value="${d.id}">${d.name}</option>`);
    if (addSel) addSel.insertAdjacentHTML("beforeend", `<option value="${d.id}">${d.name}</option>`);
  });
  $("#stat-depts").textContent = depts.length;
}

// Draw the toppers as simple CSS bars (no chart library needed).
async function loadChart() {
  const { data } = await api("/api/students/toppers/");
  const max = Math.max(1, ...data.map((s) => s.marks));
  $("#chart").innerHTML = data.map((s) => `
    <div style="margin:6px 0">
      <div class="muted" style="font-size:.85rem">${s.name} — ${s.marks}</div>
      <div class="progress"><span style="width:${(s.marks / max) * 100}%"></span></div>
    </div>`).join("") || '<p class="empty">No data yet.</p>';
}

// Load the (optionally filtered/searched) student table + stats.
async function loadStudents() {
  const q = encodeURIComponent($("#search").value.trim());
  const dept = $("#dept-filter").value;
  let url = `/api/students/?search=${q}`;
  if (dept) url += `&department=${dept}`;
  const { data } = await api(url);
  const rows = data.results || data;
  const tbody = $("#rows");
  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty">No students match.</td></tr>';
  } else {
    tbody.innerHTML = rows.map((s) => `
      <tr>
        <td>${s.roll}</td><td>${s.name}</td><td>${s.email}</td>
        <td>${s.department ? s.department.name : "—"}</td>
        <td>${s.marks}</td>
        <td><span class="badge ${s.is_active ? "ok" : "muted"}">${s.is_active ? "active" : "inactive"}</span></td>
      </tr>`).join("");
  }
  // Stats from the full (count) result when paginated, else array length.
  const total = data.count != null ? data.count : rows.length;
  $("#stat-total").textContent = total;
  const avg = rows.length ? Math.round(rows.reduce((a, s) => a + s.marks, 0) / rows.length) : 0;
  $("#stat-avg").textContent = avg;
}

function wireSearch() {
  $("#search").addEventListener("input", () => {
    clearTimeout(debounce);
    debounce = setTimeout(loadStudents, 250); // live search, debounced
  });
  $("#dept-filter").addEventListener("change", loadStudents);
}

function wireAddForm() {
  const btn = $("#add-btn");
  if (!btn) return; // anonymous visitor
  const form = $("#add-form");
  btn.addEventListener("click", () => {
    form.style.display = form.style.display === "none" ? "block" : "none";
  });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = Object.fromEntries(new FormData(form).entries());
    fd.roll = Number(fd.roll);
    fd.marks = Number(fd.marks);
    fd.department_id = Number(fd.department_id);
    const { ok, status, data } = await api("/api/students/", "POST", fd);
    const msg = $("#add-msg");
    if (ok) {
      msg.textContent = "Saved!";
      form.reset();
      loadStudents(); loadChart();
    } else if (status === 401 || status === 403) {
      msg.textContent = "You need to be logged in to add students.";
    } else {
      msg.textContent = "Error: " + JSON.stringify(data);
    }
  });
}

(async function init() {
  await loadDepartments();
  await Promise.all([loadStudents(), loadChart()]);
  wireSearch();
  wireAddForm();
})();
