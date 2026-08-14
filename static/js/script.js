/* =========================================================
   CafeHub - script.js
   Handles menu search, category filter, and price sorting
   entirely on the client side (no page reload needed).
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("menuSearch");
  const categoryPills = document.querySelectorAll(".category-pill");
  const sortSelect = document.getElementById("sortSelect");
  const menuGrid = document.getElementById("menuGrid");
  const noResults = document.getElementById("noResults");

  // If the menu grid isn't on this page, stop (avoids errors on other pages)
  if (!menuGrid) return;

  let activeCategory = "All";

  function getCards() {
    return Array.from(menuGrid.querySelectorAll(".menu-card-col"));
  }

  function applyFilters() {
    const searchTerm = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const cards = getCards();
    let visibleCount = 0;

    cards.forEach(function (card) {
      const name = card.dataset.name.toLowerCase();
      const category = card.dataset.category;

      const matchesSearch = name.includes(searchTerm);
      const matchesCategory = activeCategory === "All" || category === activeCategory;

      if (matchesSearch && matchesCategory) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    if (noResults) {
      noResults.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  function applySort() {
    if (!sortSelect) return;
    const value = sortSelect.value;
    const cards = getCards();

    if (value === "low-high") {
      cards.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
    } else if (value === "high-low") {
      cards.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
    } else {
      // "default" -> sort by original index stored in dataset
      cards.sort((a, b) => parseInt(a.dataset.index) - parseInt(b.dataset.index));
    }

    cards.forEach((card) => menuGrid.appendChild(card));
  }

  // ---- Event listeners ----
  if (searchInput) {
    searchInput.addEventListener("input", applyFilters);
  }

  categoryPills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      categoryPills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      activeCategory = pill.dataset.category;
      applyFilters();
    });
  });

  if (sortSelect) {
    sortSelect.addEventListener("change", applySort);
  }

  // Initial run
  applyFilters();
});

/* =========================================================
   Auto-dismiss flash messages after a few seconds
   ========================================================= */
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".auto-dismiss");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });
});

/* =========================================================
   Confirm before deleting a menu item (admin)
   ========================================================= */
function confirmDelete(itemName) {
  return confirm("Are you sure you want to delete '" + itemName + "'? This cannot be undone.");
}
