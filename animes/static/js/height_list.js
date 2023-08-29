window.addEventListener('DOMContentLoaded', function () {
    var colDiv = document.getElementById('col-md-2');
    var animeListDiv = document.getElementById('anime-list');

    function setColHeightToAnimeListHeight() {
        // Obtener el ancho actual de la ventana
        var windowWidth = window.innerWidth;

        // Solo ajustar la altura si el ancho es mayor que el de un dispositivo móvil (por ejemplo, 768px)
        if (windowWidth > 768) {
            colDiv.style.height = animeListDiv.clientHeight + 'px';
        } else {
            // Si es una resolución de dispositivo móvil, restablecer la altura
            colDiv.style.height = 'auto';
        }
    }

    setColHeightToAnimeListHeight();
    window.addEventListener('resize', setColHeightToAnimeListHeight);
});