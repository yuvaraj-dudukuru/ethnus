// Tiny progressive enhancement — no framework, fast load.

// Current year in the footer.
document.getElementById("year").textContent = new Date().getFullYear();

// Project cards: open the data-url in a new tab. Keeping the real URL in a
// data attribute (and href="#") means the page never shows a broken link
// before you've filled in your deployed URLs — update data-url after deploying.
document.querySelectorAll(".card[data-url]").forEach((card) => {
  card.addEventListener("click", (e) => {
    const url = card.getAttribute("data-url");
    if (url && url !== "#") {
      e.preventDefault();
      window.open(url, "_blank", "noopener");
    }
  });
});
