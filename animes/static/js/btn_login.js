// Obtén los elementos del DOM
const loginCard = document.getElementById('loginCard');
const showLoginBtn = document.getElementById('showLoginBtn');
const showLoginBtn2 = document.getElementById('showLoginBtn2');

// Variable para alternar la visibilidad del formulario
let isLoginFormVisible = false;

// Función para mostrar u ocultar el formulario
function toggleLoginForm() {
    if (isLoginFormVisible) {
        loginCard.style.display = 'none'; // Oculta el formulario
    } else {
        loginCard.style.display = 'block'; // Muestra el formulario
    }
    isLoginFormVisible = !isLoginFormVisible; // Invierte el valor de la variable
}

// Agrega los event listeners para mostrar/ocultar el formulario
showLoginBtn.addEventListener('click', toggleLoginForm);
showLoginBtn2.addEventListener('click', toggleLoginForm);

// Oculta el formulario al cargar la página
window.addEventListener('load', () => {
    loginCard.style.display = 'none'; // Oculta el formulario por defecto
});
