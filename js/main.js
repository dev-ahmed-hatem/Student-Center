const menuBtn = document.getElementById("menu-btn"),
    menu = document.getElementById("menu-side");

menuBtn.addEventListener("click", function () {
    menu.classList.toggle("active");
    menu.style.maxHeight = menu.classList.contains("active")
        ? menu.scrollHeight + "px"
        : 0;
});

document.body.addEventListener("click", (event) => {
    if (
        !menu.contains(event.target) &&
        event.target !== menuBtn &&
        menu.classList.contains("active")
    ) {
        menuBtn.click();
    }
});
