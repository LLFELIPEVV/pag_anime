const footer = document.querySelector('.footer');
const pageContent = document.querySelector('.page-content');

// Función para posicionar el footer
function positionFooter() {
    const pageContentRect = pageContent.getBoundingClientRect();
    const footerHeight = footer.offsetHeight;
    const windowHeight = window.innerHeight;

    const bottomOfPageContent = pageContentRect.top + pageContentRect.height + 7; // Agregamos 7px de margen

    // Ajustar la posición para asegurarse de que el footer termine en el final del 100vh
    if (bottomOfPageContent < windowHeight) {
        bottomOfPageContent = windowHeight;
    }

    footer.style.position = 'absolute';
    footer.style.top = `${bottomOfPageContent}px`; // Establece el valor de top
}

// Función para llevar al usuario al principio de la página
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Agrega un desplazamiento suave
    });
}

// Esta función se llamará cada vez que se haga clic en un botón con la clase 'mobile-button' o enlace con la clase 'nav-link-usuarios'
function reloadFooterPosition() {
    positionFooter();
}

// Agregar un evento de clic a cada botón con la clase 'mobile-button' y enlace con la clase 'nav-link-usuarios'
function attachButtonAndNavLinksListeners() {
    document.querySelectorAll('.mobile-button, .nav-link-usuarios').forEach(element => {
        element.addEventListener('click', (event) => {
            if (element.classList.contains('nav-link-usuarios')) {
                event.preventDefault(); // Evitar la acción predeterminada de navegación solo para enlaces
            }
            reloadFooterPosition();
        });
    });
}

// Llamada a las funciones cuando la página se carga
window.addEventListener('load', () => {
    scrollToTop();
    positionFooter(); // Llamamos a la función de posicionamiento del footer
    attachButtonAndNavLinksListeners(); // Agregar los eventos de clic a los botones móviles y enlaces
});

// Llamada a la función de posicionamiento del footer cuando cambia el tamaño de la ventana
window.addEventListener('resize', () => {
    positionFooter();
    reloadFooterPosition(); // Asegurarse de que la posición también se recargue al cambiar el tamaño de la ventana
});