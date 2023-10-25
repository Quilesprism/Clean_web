document.getElementById("toggle-nav").addEventListener("click", function() {
    console.log("Se hizo clic en el botón");
    var navbarList = document.getElementById("navbar-list");
    navbarList.classList.toggle("show");
});
