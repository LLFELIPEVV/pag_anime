document.addEventListener("DOMContentLoaded", function() {
    var slider = document.getElementById("slider");
    var images = slider.querySelectorAll("img");

    images.forEach(function(image) {
        image.addEventListener("error", function() {
            this.onerror = null; // Evita bucles infinitos en caso de múltiples errores
            this.src = "/static/images/negro.jpg"; // Reemplaza con la ruta correcta
        });
    });
});
