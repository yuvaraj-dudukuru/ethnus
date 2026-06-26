// jobs.js — job search, recruiter posting, candidate apply (file upload).
const $ = (s) => document.querySelector(s);
let debounce;

async function loadJobs() {
  const q = encodeURIComponent($("#search").value.trim());
  const loc = encodeURIComponent($("#loc").value.trim());
  const type = $("#type").value;
  let url = `/api/jobs/?search=${q}`;
  if (loc) url += `&location=${loc}`;
  if (type) url += `&type=${type}`;
  const { data } = await api(url);
  const jobs = data.results || data;
  const wrap = $("#jobs");
  if (!jobs.length) { wrap.innerHTML = '<p class="empty">No jobs found.</p>'; return; }
  wrap.innerHTML = jobs.map((j) => `
    <div class="card">
      <h3>${j.title} <span class="badge muted">${j.type_display}</span></h3>
      <p class="muted">${j.company} · ${j.location} ${j.salary ? "· $" + j.salary : ""}</p>
      <p>${j.description}</p>
      <p class="muted">Posted by ${j.recruiter} · ${j.application_count} applicant(s)</p>
      ${actions(j)}
    </div>`).join("");
  wireCards();
}

function actions(j) {
  if (window.ROLE === "candidate") {
    return `
      <button class="btn primary small" data-apply="${j.id}">Apply</button>
      <form class="apply-form" data-form="${j.id}" style="display:none;margin-top:10px">
        <label>Resume (file)<input type="file" name="resume" required></label>
        <label>Cover note<textarea name="cover_note" rows="2"></textarea></label>
        <button class="btn ok small" type="submit">Send application</button>
        <span class="msg muted"></span>
      </form>`;
  }
  if (window.ROLE === "recruiter" && j.recruiter === window.USERNAME) {
    return `<button class="btn small" data-applicants="${j.id}">View applicants</button>
            <div class="applicants" data-list="${j.id}"></div>`;
  }
  return "";
}

function wireCards() {
  document.querySelectorAll("[data-apply]").forEach((b) =>
    b.addEventListener("click", () => {
      const f = document.querySelector(`[data-form="${b.dataset.apply}"]`);
      f.style.display = f.style.display === "none" ? "block" : "none";
    }));
  document.querySelectorAll(".apply-form").forEach((form) =>
    form.addEventListener("submit", (e) => submitApply(e, form)));
  document.querySelectorAll("[data-applicants]").forEach((b) =>
    b.addEventListener("click", () => loadApplicants(b.dataset.applicants)));
}

async function submitApply(e, form) {
  e.preventDefault();
  const fd = new FormData(form);  // multipart (includes the file)
  const res = await fetch(`/api/jobs/${form.dataset.form}/apply/`, {
    method: "POST", headers: { "X-CSRFToken": window.CSRF }, body: fd,
  });
  const data = await res.json().catch(() => ({}));
  form.querySelector(".msg").textContent = res.ok
    ? "Applied!" : (data.detail || "Could not apply.");
  if (res.ok) loadJobs();
}

async function loadApplicants(jobId) {
  const box = document.querySelector(`[data-list="${jobId}"]`);
  const { ok, data } = await api(`/api/jobs/${jobId}/applicants/`);
  if (!ok) { box.innerHTML = '<p class="muted">Could not load.</p>'; return; }
  box.innerHTML = data.length ? `<table><thead><tr><th>Candidate</th><th>Status</th><th>Resume</th></tr></thead><tbody>${
    data.map((a) => `<tr><td>${a.candidate}</td><td>${a.status}</td><td><a href="${a.resume}">resume</a></td></tr>`).join("")
  }</tbody></table>` : '<p class="empty">No applicants yet.</p>';
}

function wirePostForm() {
  const form = $("#post-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = Object.fromEntries(new FormData(form).entries());
    if (body.salary === "") delete body.salary;
    const { ok, data } = await api("/api/jobs/", "POST", body);
    $("#post-msg").textContent = ok ? "Published!" : JSON.stringify(data);
    if (ok) { form.reset(); loadJobs(); }
  });
}

["#search", "#loc"].forEach((s) => $(s).addEventListener("input", () => {
  clearTimeout(debounce); debounce = setTimeout(loadJobs, 250);
}));
$("#type").addEventListener("change", loadJobs);

(function init() { loadJobs(); wirePostForm(); })();
