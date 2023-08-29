function showContent(contentId) {
    if (window.innerWidth <= 767) {
        // Ocultar todos los contenidos primero
        document.querySelectorAll('.row-main > div').forEach(div => {
            div.style.display = 'none';
        });

        // Mostrar el contenido seleccionado
        document.querySelector('.' + contentId).style.display = 'block';

        // Cambiar la clase activa del botón
        document.querySelectorAll('.mobile-button').forEach(button => {
            button.classList.remove('active');
        });
        document.querySelector('[onclick="showContent(\'' + contentId + '\')"]').classList.add('active');
    }
}

// Mostrar el contenido por defecto al cargar la página
showDefaultContent();

function showDefaultContent() {
    if (window.innerWidth <= 767) {
        document.querySelector('.col-md-2').style.display = 'block';
        document.querySelector('.col-md-8').style.display = 'none';
        document.querySelector('.lastest-animes').style.display = 'none';
    }
}
