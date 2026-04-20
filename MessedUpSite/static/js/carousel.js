document.querySelectorAll(".carousel").forEach(carousel => {
  const items = carousel.querySelectorAll(".item");
  const buttonsHtml = Array.from(items, () => {
    return `<span class="carousel-button"></span>`;
  });

  carousel.insertAdjacentHTML("beforeend", `
    <div class="carousel-nav"> 
        ${ buttonsHtml.join("") }
    </div>
    `);

    const buttons = carousel.querySelectorAll(".carousel-button");

    let currentIndex = 0;
    let intervalId;

    function selectItem(index) {
      items.forEach(item => item.classList.remove("carousel-selected"));
      buttons.forEach(button => button.classList.remove("button-selected"));

      items[index].classList.add("carousel-selected");
      buttons[index].classList.add("button-selected");
      currentIndex = index;
    }

    function startRotation() {
      intervalId = setInterval(() => {
        const nextIndex = (currentIndex + 1) % items.length;
        selectItem(nextIndex);
      }, 10000);
    }

    buttons.forEach((button, i) => {
      button.addEventListener("click", () => {
        clearInterval(intervalId);
        selectItem(i);
        startRotation();
      });
    });

  selectItem(0);
  startRotation();

});



