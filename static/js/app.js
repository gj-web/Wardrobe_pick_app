// Wardrobe Pick — app.js

document.addEventListener("DOMContentLoaded", () => {

  // ── Form loading state ──────────────────────────────────────────
  const form = document.getElementById("tripForm");
  const submitBtn = document.getElementById("submitBtn");

  if (form && submitBtn) {
    form.addEventListener("submit", () => {
      const btnText = submitBtn.querySelector(".btn-text");
      const btnIcon = submitBtn.querySelector(".btn-icon");
      const loader  = submitBtn.querySelector(".btn-loader");

      if (btnText) btnText.textContent = "Building…";
      if (btnIcon) btnIcon.classList.add("hidden");
      if (loader)  loader.classList.remove("hidden");

      submitBtn.disabled = true;
      submitBtn.style.pointerEvents = "none";
    });
  }

  // ── Staggered card entrance on results page ─────────────────────
  const cards = document.querySelectorAll(".outfit-card");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    cards.forEach((card) => {
      card.style.opacity = "0";
      observer.observe(card);
    });
  }

  // ── Destination field auto-capitalise ──────────────────────────
  const destInput = document.getElementById("destination");
  if (destInput) {
    destInput.addEventListener("blur", () => {
      destInput.value = destInput.value
        .split(" ")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
        .join(" ");
    });
  }

});
