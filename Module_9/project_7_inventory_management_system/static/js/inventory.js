// inventory.js — live stock dashboard with polling, low-stock highlighting,
// stock in/out actions, a CSS bar chart and a movement history feed.
const $ = (s) => document.querySelector(s);
let debounce;

async function loadProducts() {
  const q = encodeURIComponent($("#search").value.trim());
  let url = `/api/products/?search=${q}`;
  if ($("#only-low").checked) url += "&low_stock=true";
  const { data } = await api(url);
  const products = data.results || data;
  // Stats
  $("#stat-products").textContent = data.count != null ? data.count : products.length;
  $("#stat-low").textContent = products.filter((p) => p.low_stock).length;
  $("#stat-units").textContent = products.reduce((a, p) => a + p.quantity, 0);
  // Table
  const tbody = $("#rows");
  tbody.innerHTML = products.length ? products.map((p) => `
    <tr style="${p.low_stock ? "background:#fff7ed" : ""}">
      <td>${p.name}</td><td>${p.sku}</td><td>${p.quantity}</td><td>${p.reorder_level}</td>
      <td><span class="badge ${p.low_stock ? "warn" : "ok"}">${p.low_stock ? "reorder" : "ok"}</span></td>
      ${window.LOGGED_IN ? `<td class="row-actions">
        <button class="btn ok small" data-in="${p.id}">+ In</button>
        <button class="btn bad small" data-out="${p.id}">– Out</button></td>` : ""}
    </tr>`).join("") : '<tr><td colspan="6" class="empty">No products.</td></tr>';
  // Chart (CSS bars)
  const max = Math.max(1, ...products.map((p) => p.quantity));
  $("#chart").innerHTML = products.slice(0, 10).map((p) => `
    <div style="margin:6px 0">
      <div class="muted" style="font-size:.85rem">${p.name} — ${p.quantity}</div>
      <div class="progress"><span style="width:${(p.quantity / max) * 100}%;background:${p.low_stock ? "#d97706" : "#16a34a"}"></span></div>
    </div>`).join("");
  wireActions();
}

function wireActions() {
  document.querySelectorAll("[data-in]").forEach((b) =>
    b.addEventListener("click", () => move(b.dataset.in, "stock_in")));
  document.querySelectorAll("[data-out]").forEach((b) =>
    b.addEventListener("click", () => move(b.dataset.out, "stock_out")));
}

async function move(id, kind) {
  const qty = prompt(`Quantity to ${kind === "stock_in" ? "add" : "remove"}?`, "1");
  if (!qty) return;
  const { ok, data } = await api(`/api/products/${id}/${kind}/`, "POST", { qty: Number(qty) });
  if (!ok) alert(data.detail || "Failed.");
  await refresh();
}

async function loadMovements() {
  const { data } = await api("/api/movements/?type=");
  const moves = (data.results || data).slice(0, 10);
  $("#moves").innerHTML = `<thead><tr><th>When</th><th>Product</th><th>Type</th><th>Qty</th></tr></thead><tbody>${
    moves.map((m) => `<tr><td>${new Date(m.date).toLocaleString()}</td><td>${m.product_name}</td>
      <td><span class="badge ${m.type === "IN" ? "ok" : "muted"}">${m.type}</span></td><td>${m.qty}</td></tr>`).join("")
    || '<tr><td colspan="4" class="empty">No movements yet.</td></tr>'}</tbody>`;
}

async function refresh() { await Promise.all([loadProducts(), loadMovements()]); }

$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadProducts, 250); });
$("#only-low").addEventListener("change", loadProducts);

refresh();
setInterval(refresh, 8000); // real-time-ish polling
