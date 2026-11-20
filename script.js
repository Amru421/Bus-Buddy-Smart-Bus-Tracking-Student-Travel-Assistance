document.addEventListener("DOMContentLoaded", function () {

    // Mobile navigation
    const menu = document.querySelector(".menu-toggle");
    const nav = document.querySelector(".nav-links");

    if (menu && nav) {
        menu.addEventListener("click", function () {
            nav.classList.toggle("active");
        });
    }

    // Confirm logout
    document.querySelectorAll(".logout-link").forEach(link => {
        link.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to logout?")) {
                event.preventDefault();
            }
        });
    });

});
