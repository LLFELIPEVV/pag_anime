document.addEventListener("DOMContentLoaded", function () {
    const videoButtons = document.querySelectorAll(".option-button");

    // Establece la fuente del iframe al cargar la página
    const videoIframe = document.getElementById("video-iframe");

    // Función para manejar los clics en los botones
    function handleButtonClick(event) {
        const clickedButton = event.currentTarget;
        const buttonSrc = clickedButton.getAttribute("data-src");

        // Cambia la fuente del iframe
        videoIframe.src = buttonSrc;

        // Actualiza las clases "active" y "play-button" en los botones
        videoButtons.forEach(button => {
            button.classList.remove("active", "play-button");
        });
        clickedButton.classList.add("active", "play-button");
    }

    // Agrega un evento de clic a cada botón
    videoButtons.forEach(button => {
        button.addEventListener("click", handleButtonClick);
    });

    // Establece el primer botón como activo por defecto
    const defaultButton = videoButtons[0];
    defaultButton.click(); // Simula un clic en el primer botón al cargar la página
});
