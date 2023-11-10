// Obtén los elementos del DOM
const avatars = document.querySelectorAll('.avatar');
const loginButtons = document.querySelectorAll('.btn-login');
const loginCard = document.getElementById('loginCard');

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

// Agrega los event listeners para mostrar/ocultar el formulario a cada avatar y botón de inicio de sesión
avatars.forEach(avatar => {
    avatar.addEventListener('click', toggleLoginForm);
});

loginButtons.forEach(button => {
    button.addEventListener('click', toggleLoginForm);
});

// Oculta el formulario al cargar la página
window.addEventListener('load', () => {
    loginCard.style.display = 'none'; // Oculta el formulario por defecto
});

