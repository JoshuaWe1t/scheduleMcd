const btnLogout = document.getElementById("btn-log-out");

btnLogout.addEventListener('click', e => {
    localStorage.clear();
    window.location.href = "login.html";
})
