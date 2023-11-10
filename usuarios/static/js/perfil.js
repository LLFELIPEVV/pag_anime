document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".nav-link-usuarios");

    links.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            // Oculta todos los contenidos
            document.querySelectorAll(".content-ventanas").forEach(function (content) {
                content.classList.remove("active");
            });

            // Muestra el contenido correspondiente al enlace clicado
            const targetId = link.getAttribute("data-target");
            const targetContent = document.getElementById(targetId);

            if (targetContent) {
                targetContent.classList.add("active");
            }
        });
    });
});
