const footer = document.querySelector('.footer');
const pageContent = document.querySelector('.page-content');

// Función para posicionar el footer
function positionFooter() {
    const pageContentRect = pageContent.getBoundingClientRect();
    const footerHeight = footer.offsetHeight;
    
    const bottomOfPageContent = pageContentRect.top + pageContentRect.height + 7; // Agregamos 7px de margen

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

// Llamada a las funciones cuando la página se carga
window.addEventListener('load', () => {
    scrollToTop();
    positionFooter(); // Llamamos a la función de posicionamiento del footer
});

// Llamada a la función de posicionamiento del footer cuando cambia el tamaño de la ventana
window.addEventListener('resize', positionFooter);




