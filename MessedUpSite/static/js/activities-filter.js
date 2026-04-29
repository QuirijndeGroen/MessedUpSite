function FilterActivities() {
  document.getElementsByName("activity_type").forEach((radio) => {
    radio.addEventListener("change", () => {
      const selectedValue = radio.value;
      const activityCards = document.querySelectorAll(".activity");

      activityCards.forEach((card) => {
        const cardType = card.getAttribute("title");
        if (selectedValue === "all" || cardType === selectedValue) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  document.getElementById("search_input").addEventListener("input", (event) => {
    const searchTerm = event.target.value.toLowerCase();
    const activityCards = document.querySelectorAll(".activity");

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


