document.addEventListener('DOMContentLoaded', function () {
    const downloadButton = document.getElementById('download-button');
    const downloadLinks = document.getElementById('download-links');
    const aviso = document.getElementById('sin_links');
    
    // Verificar si hay filas en la tabla
    const tabla = document.querySelector('.RTbl tbody');
    const filas = tabla.getElementsByTagName('tr');
    
    // Mostrar el mensaje si no hay filas en la tabla
    if (filas.length === 0) {
        aviso.style.display = 'block';
    }

    downloadButton.addEventListener('click', function () {
        // Verifica el estado actual del div de enlaces y cambia su visibilidad
        if (downloadLinks.style.display === 'none' || downloadLinks.style.display === '') {
            downloadLinks.style.display = 'block'; // Mostrar los enlaces
        } else {
            downloadLinks.style.display = 'none'; // Ocultar los enlaces
        }
    });
});
