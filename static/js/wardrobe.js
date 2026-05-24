// Wardrobe Pick — wardrobe.js
// Handles: image upload preview, outfit filter, and form validation

document.addEventListener("DOMContentLoaded", () => {

  // ── Image Upload Preview ────────────────────────────────────────
  const uploadInput  = document.getElementById("image");
  const uploadPreview = document.getElementById("uploadPreview");
  const uploadPlaceholder = document.getElementById("uploadPlaceholder");
  const uploadArea   = document.getElementById("uploadArea");

  if (uploadInput && uploadPreview) {
    // Click on upload area opens file picker
    uploadArea.addEventListener("click", (e) => {
      if (e.target !== uploadInput) uploadInput.click();
    });

    uploadInput.addEventListener("change", () => {
      const file = uploadInput.files[0];
      if (!file) return;

      // Size check (5 MB)
      if (file.size > 5 * 1024 * 1024) {
        alert("Photo is too large. Please choose a file under 5 MB.");
        uploadInput.value = "";
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        uploadPreview.src = e.target.result;
        uploadPreview.classList.remove("hidden");
        uploadPlaceholder.classList.add("hidden");
      };
      reader.readAsDataURL(file);
    });

    // Drag & drop support
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.classList.add("drag-over");
    });
    uploadArea.addEventListener("dragleave", () => {
      uploadArea.classList.remove("drag-over");
    });
    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.classList.remove("drag-over");
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith("image/")) {
        const dt = new DataTransfer();
        dt.items.add(file);
        uploadInput.files = dt.files;
        uploadInput.dispatchEvent(new Event("change"));
      }
    });
  }

  // ── Add Outfit Form Loading State ──────────────────────────────
  const addForm = document.getElementById("addOutfitForm");
  const addBtn  = document.getElementById("addBtn");

  if (addForm && addBtn) {
    addForm.addEventListener("submit", () => {
      const btnText = addBtn.querySelector(".btn-text");
      if (btnText) btnText.textContent = "Adding…";
      addBtn.disabled = true;
    });
  }

  // ── Outfit Category Filter ──────────────────────────────────────
  const filterBtns = document.querySelectorAll(".filter-btn");
  const wardrobeGrid = document.getElementById("wardrobeGrid");

  if (filterBtns.length && wardrobeGrid) {
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.dataset.filter;

        // Toggle active state
        filterBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");

        // Show/hide cards
        const cards = wardrobeGrid.querySelectorAll(".my-outfit-card");
        cards.forEach((card) => {
          if (filter === "all" || card.dataset.category === filter) {
            card.style.display = "";
            card.style.opacity = "1";
          } else {
            card.style.display = "none";
          }
        });
      });
    });
  }

  // ── Staggered card entrance ─────────────────────────────────────
  const myCards = document.querySelectorAll(".my-outfit-card");
  if ("IntersectionObserver" in window && myCards.length) {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const delay = entry.target.style.getPropertyValue("--card-index") * 60;
            setTimeout(() => {
              entry.target.style.opacity = "1";
              entry.target.style.transform = "translateY(0)";
            }, delay);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05 }
    );
    myCards.forEach((card) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(20px)";
      card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      obs.observe(card);
    });
  }

});
