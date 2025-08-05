document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector("#searchForm");
  const searchInput = document.querySelector("#searchInput");
  const resultsContainer = document.querySelector("#results");

  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;

    // Llamada a backend Flask para obtener resultados de búsqueda
    try {
      const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      displayResults(data.tracks);
    } catch (error) {
      console.error("Error al buscar canciones:", error);
    }
  });

  function displayResults(tracks) {
    resultsContainer.innerHTML = "";
    tracks.forEach((track) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <h1>${track.name}</h1>
        <p><strong>Artista:</strong> ${track.artist}</p>
        <img src="${track.image}" alt="${track.name}" width="100%">
        ${track.preview_url ? `<audio controls src="${track.preview_url}"></audio>` : '<p>Sin preview</p>'}
      `;
      resultsContainer.appendChild(card);
    });
  }
});
