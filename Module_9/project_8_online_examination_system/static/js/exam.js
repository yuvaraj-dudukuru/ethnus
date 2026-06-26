// exam.js — list exams, take one with a live countdown, auto-submit, results.
const $ = (s) => document.querySelector(s);
let timer, currentExam;

function show(view) {
  ["list-view", "take-view", "result-view"].forEach((v) =>
    $("#" + v).style.display = v === view ? "block" : "none");
}

async function loadExams() {
  const { data } = await api("/api/exams/");
  const exams = data.results || data;
  $("#exams").innerHTML = exams.length ? exams.map((e) => `
    <div class="card">
      <h3>${e.title}</h3>
      <p class="muted">${e.question_count} questions · ${e.duration} min · ${e.max_marks} marks</p>
      ${window.LOGGED_IN ? `<button class="btn primary small" data-start="${e.id}">Start exam</button>`
                          : '<a class="btn small" href="/login/">Log in to take</a>'}
    </div>`).join("") : '<p class="empty">No exams available.</p>';
  $("#exams").querySelectorAll("[data-start]").forEach((b) =>
    b.addEventListener("click", () => startExam(b.dataset.start)));
}

async function startExam(id) {
  const { ok, data } = await api(`/api/exams/${id}/start/`, "POST");
  if (!ok) { alert(data.detail || "Cannot start."); return; }
  currentExam = id;
  $("#exam-title").textContent = "Exam in progress";
  $("#quiz").innerHTML = data.questions.map((q, i) => `
    <div class="card">
      <p><b>Q${i + 1}.</b> ${q.text} <span class="muted">(${q.marks} mark)</span></p>
      ${q.choices.map((c) => `
        <label style="color:inherit"><input type="radio" name="q${q.id}" value="${c.id}" style="width:auto"> ${c.text}</label>`).join("")}
    </div>`).join("");
  show("take-view");
  startCountdown(new Date(data.deadline));
}

function startCountdown(deadline) {
  clearInterval(timer);
  timer = setInterval(() => {
    const left = Math.max(0, Math.floor((deadline - new Date()) / 1000));
    const m = String(Math.floor(left / 60)).padStart(2, "0");
    const s = String(left % 60).padStart(2, "0");
    $("#timer").textContent = `${m}:${s}`;
    if (left <= 0) { clearInterval(timer); submitExam(); }  // auto-submit on timeout
  }, 1000);
}

function collectAnswers() {
  const answers = [];
  $("#quiz").querySelectorAll('input[type="radio"]:checked').forEach((r) =>
    answers.push({ question: Number(r.name.slice(1)), choice: Number(r.value) }));
  return answers;
}

async function submitExam() {
  clearInterval(timer);
  const { data } = await api(`/api/exams/${currentExam}/submit/`, "POST",
    { answers: collectAnswers() });
  $("#result").textContent = data.expired
    ? `Time expired! Score: ${data.score} / ${data.total}`
    : `You scored ${data.score} / ${data.total}`;
  show("result-view");
  loadExams();
}

$("#submit-btn").addEventListener("click", submitExam);
$("#cancel-btn").addEventListener("click", () => { clearInterval(timer); show("list-view"); });
$("#done-btn").addEventListener("click", () => show("list-view"));

loadExams();
