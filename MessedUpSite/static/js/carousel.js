document.querySelectorAll(".carousel").forEach(carousel => {
  const items = carousel.querySelectorAll(".card-carousel");
  const buttonsHtml = Array.from(items, () => {
    return `<span class="carousel-button"></span>`;
  });

  carousel.insertAdjacentHTML("beforeend", `
    <div class="carousel-nav"> 
        ${ buttonsHtml.join("") }
    </div>
    `);

    const buttons = carousel.querySelectorAll(".carousel-button");

    buttons.forEach((button, i) => {
      button.addEventListener("click", () => {
        items.forEach(item => item.classList.remove("carousel-selected"));
        buttons.forEach(button => button.classList.remove("button-selected")); 

        items[i].classList.add("carousel-selected");
        button.classList.add("button-selected");
      });
    });

  items[0].classList.add("carousel-selected");
  buttons[0].classList.add("button-selected");

});



