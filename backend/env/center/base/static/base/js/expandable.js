function toggle(el) {
    let contentContainer = el.parentElement.parentElement.querySelector(
        ".content"
    );
    el.classList.contains("active")
        ? (() => {
              el.classList.remove("active");
              el.querySelector(".text").innerHTML = "عرض";
              contentContainer.style.maxHeight = 0;
          })()
        : (() => {
              el.querySelector(".text").innerHTML = "إخفاء";
              el.classList.add("active");
              contentContainer.style.maxHeight =
                  contentContainer.scrollHeight + "px";
          })();
}

window.onload = function () {
    document.querySelectorAll(".expandable .title").forEach((el) => {
        el.addEventListener("click", () => {
            toggle(el.querySelector(".toggle"));
        });
    });
};
