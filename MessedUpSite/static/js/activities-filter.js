function FilterActivities() {
  document.getElementsByName("activity_type").forEach((radio) => {
    radio.addEventListener("change", () => {
      const selectedValue = radio.value;
      const activityCards = document.querySelectorAll(".card.item");

      activityCards.forEach((card) => {
        const cardType = card.getAttribute("title");
        if (selectedValue === "all" || cardType === selectedValue) {
          card.style.display = "grid";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}

FilterActivities();