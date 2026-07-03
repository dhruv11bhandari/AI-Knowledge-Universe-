// main.js
// A few small UI touches. Nothing complex - most of the interesting
// interactivity (search, graph) is handled server-side or by PyVis.

document.addEventListener("DOMContentLoaded", function () {
  // Auto-focus the search input on the search page so users can start
  // typing immediately.
  const searchInput = document.querySelector(".search-form input");
  if (searchInput && !searchInput.value) {
    searchInput.focus();
  }
});
