function FilterActivities() {
  document.getElementById("search_input").addEventListener("input", (event) => {
    const searchTerm = event.target.value.toLowerCase();
    const activityCards = document.querySelectorAll(".quote");

    activityCards.forEach((card) => {
      const cardText = card.textContent.toLowerCase();
      if (cardText.includes(searchTerm)) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });
  });
}

FilterActivities();


