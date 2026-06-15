let modalIntroduction = document.querySelector(".modal-introduction"),
    modalAbout = document.querySelector(".modal-about"),
    closeButton = document.querySelector(".close-button"),
    intro = document.getElementById("introduction"),
    about = document.getElementById("about");

function toggleModalIntro() {
    modalIntroduction.classList.toggle("show-modal");
}

function toggleModalAbout() {
    modalAbout.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modalIntroduction) {
        toggleModalIntro();
    } else if (event.target === modalAbout) {
        toggleModalAbout();
    }
}

intro.addEventListener("click", toggleModalIntro);
about.addEventListener("click", toggleModalAbout);
window.addEventListener("click", windowOnClick);