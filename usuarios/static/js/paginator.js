document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".nav-link-usuarios");
    let lastClickedLinkId = localStorage.getItem("lastClickedLinkId");

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

                // Guarda el ID del último enlace clicado en el almacenamiento local
                lastClickedLinkId = targetId;
                localStorage.setItem("lastClickedLinkId", lastClickedLinkId);

                // Encuentra el botón con name="enviar" más cercano al targetContent
                const button = targetContent.querySelector('[name="enviar"]');

                // Encuentra el div con name="menu-desplegable" más cercano al targetContent
                const menu = targetContent.querySelector('[name="menu-desplegable"]');

                // Verifica si se encontró un botón
                if (button) {
                    // Establece el atributo data-form solo para ese botón
                    button.setAttribute("data-form", targetId);
                    // Establece el id unicamente para ese div
                    menu.id = "menu-" + targetId;
                } else {
                    console.error("No se encontró el botón 'enviar' asociado al enlace clicado.");
                }
            }
        });
    });

    // Si se ha guardado el ID del último enlace clicado, activa ese enlace
    if (lastClickedLinkId) {
        const lastClickedLink = document.querySelector(`[data-target="${lastClickedLinkId}"]`);
        if (lastClickedLink) {
            lastClickedLink.click();
        }
    }
});
