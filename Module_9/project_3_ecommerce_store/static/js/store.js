// store.js — catalog browsing, AJAX add-to-cart, live cart badge, checkout.
const $ = (s) => document.querySelector(s);
let debounce;

async function loadCategories() {
  const { data } = await api("/api/categories/");
  const cats = data.results || data;
  cats.forEach((c) =>
    $("#cat-filter").insertAdjacentHTML("beforeend",
      `<option value="${c.id}">${c.name}</option>`));
}

async function loadProducts() {
  const q = encodeURIComponent($("#search").value.trim());
  let url = `/api/products/?search=${q}`;
  const cat = $("#cat-filter").value;
  const maxp = $("#max-price").value;
  if (cat) url += `&category=${cat}`;
  if (maxp) url += `&max_price=${maxp}`;
  const { data } = await api(url);
  const products = data.results || data;
  const wrap = $("#products");
  if (!products.length) { wrap.innerHTML = '<p class="empty">No products.</p>'; return; }
  wrap.innerHTML = products.map((p) => `
    <div class="card">
      ${p.image ? `<img src="${p.image}" alt="" style="width:100%;border-radius:8px">` : ""}
      <h3>${p.name}</h3>
      <p class="muted">${p.category ? p.category.name : ""}</p>
      <p class="price">$${p.price}</p>
      <p><span class="badge ${p.in_stock ? "ok" : "bad"}">${p.in_stock ? p.stock + " in stock" : "sold out"}</span></p>
      ${window.LOGGED_IN ? `<button class="btn primary small" ${p.in_stock ? "" : "disabled"} data-add="${p.id}">Add to cart</button>` : ""}
    </div>`).join("");
  wrap.querySelectorAll("[data-add]").forEach((b) =>
    b.addEventListener("click", () => addToCart(b.dataset.add)));
}

async function addToCart(productId) {
  const { ok, data } = await api("/api/cart/add/", "POST", { product_id: Number(productId), qty: 1 });
  if (!ok) { alert(data && data.detail ? data.detail : "Could not add."); return; }
  renderCart(data);
}

async function loadCart() {
  if (!window.LOGGED_IN) return;
  const { data } = await api("/api/cart/");
  renderCart(data);
}

function renderCart(cart) {
  $("#cart-badge").textContent = "Cart: " + (cart.count || 0);
  const box = $("#cart");
  if (!box) return;
  if (!cart.items || !cart.items.length) {
    box.innerHTML = '<p class="empty">Empty.</p>';
    $("#cart-total").textContent = "";
    $("#checkout-btn").disabled = true;
    return;
  }
  box.innerHTML = cart.items.map((i) => `
    <div class="toolbar">
      <span class="grow">${i.product.name} × ${i.qty}</span>
      <span class="price">$${i.subtotal}</span>
      <button class="btn bad small" data-remove="${i.product.id}">Remove</button>
    </div>`).join("");
  $("#cart-total").textContent = "Total: $" + cart.total;
  $("#checkout-btn").disabled = false;
  box.querySelectorAll("[data-remove]").forEach((b) =>
    b.addEventListener("click", async () => {
      const { data } = await api("/api/cart/remove/", "POST", { product_id: Number(b.dataset.remove) });
      renderCart(data);
    }));
}

function wireCheckout() {
  const btn = $("#checkout-btn");
  if (!btn) return;
  btn.addEventListener("click", async () => {
    const { ok, data } = await api("/api/cart/checkout/", "POST");
    const msg = $("#checkout-msg");
    if (ok) { msg.textContent = `Order #${data.id} placed — $${data.total}!`; loadCart(); loadProducts(); }
    else { msg.textContent = data && data.detail ? data.detail : "Checkout failed."; }
  });
}

$("#search").addEventListener("input", () => { clearTimeout(debounce); debounce = setTimeout(loadProducts, 250); });
$("#cat-filter").addEventListener("change", loadProducts);
$("#max-price").addEventListener("change", loadProducts);

(async function init() {
  await loadCategories();
  await loadProducts();
  await loadCart();
  wireCheckout();
})();
