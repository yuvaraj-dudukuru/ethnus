// lms.js — browse courses, enrol, watch lessons, track progress.
const $ = (s) => document.querySelector(s);
let debounce;

async function loadCourses() {
  const q = encodeURIComponent($("#search").value.trim());
  const { data } = await api(`/api/courses/?search=${q}`);
  const courses = data.results || data;
  const wrap = $("#courses");
  wrap.innerHTML = courses.length ? courses.map((c) => `
    <div class="card">
      <h3>${c.title}</h3>
      <p class="muted">by ${c.instructor} · ${c.lesson_count} lesson(s)</p>
      <p>${c.description || ""}</p>
      <button class="btn primary small" data-open="${c.id}">Open</button>
      ${window.LOGGED_IN ? `<button class="btn ok small" data-enroll="${c.id}">Enrol</button>` : ""}
    </div>`).join("") : '<p class="empty">No courses.</p>';
  wrap.querySelectorAll("[data-open]").forEach((b) =>
    b.addEventListener("click", () => openCourse(b.dataset.open)));
  wrap.querySelectorAll("[data-enroll]").forEach((b) =>
    b.addEventListener("click", async () => {
      const { ok, data } = await api(`/api/courses/${b.dataset.enroll}/enroll/`, "POST");
      alert(ok ? "Enrolled!" : (data.detail || "Could not enrol."));
    }));
}

async function openCourse(id) {
  const { data: course } = await api(`/api/courses/${id}/`);
  $("#courses").parentElement.style.display = "none";
  $("#detail").style.display = "block";
  $("#d-title").textContent = course.title;
  $("#d-meta").textContent = `by ${course.instructor}`;
  const { data: lessonData } = await api(`/api/lessons/?course=${id}`);
  const lessons = lessonData.results || lessonData;
  $("#lessons").innerHTML = lessons.map((l) => `
    <div class="toolbar">
      <span class="grow"><b>${l.order}.</b> ${l.title}
        ${l.video_url ? `· <a href="${l.video_url}" target="_blank">video</a>` : ""}</span>
      ${window.LOGGED_IN ? `<button class="btn ok small" data-complete="${l.id}">Mark complete</button>` : ""}
    </div>`).join("") || '<p class="empty">No lessons yet.</p>';
  $("#lessons").querySelectorAll("[data-complete]").forEach((b) =>
    b.addEventListener("click", async () => {
      const { ok, data } = await api(`/api/lessons/${b.dataset.complete}/complete/`, "POST");
      if (ok) renderProgress(data); else alert("Enrol first to track progress.");
    }));
  if (window.LOGGED_IN) {
    const { data: p } = await api(`/api/courses/${id}/progress/`);
    renderProgress(p);
  }
}

function renderProgress(p) {
  const bar = $("#d-bar");
  if (!bar) return;
  bar.style.width = p.percent + "%";
  $("#d-pct").textContent = `${p.completed}/${p.total} lessons · ${p.percent}% complete`;
}

$("#back").addEventListener("click", () => {
  $("#detail").style.display = "none";
  $("#courses").parentElement.style.display = "block";
});
$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadCourses, 250); });

loadCourses();
