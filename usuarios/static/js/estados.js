/* function enviarFormulario() {
    // Obtiene el botón con el atributo data-form establecido
    const button = document.querySelector('[name="enviar"][data-form]');
    
    // Verifica si se encontró un botón
    if (button) {
        console.log("Boton encontrado")
        const containerId = button.getAttribute("data-form");
        const formulario = document.getElementById("form-" + containerId);

        // Verifica si se encontró el formulario
        if (formulario) {
            console.log("Formulario encontrado");

            // Envía el formulario
            formulario.submit();
        } else {
            console.error("No se encontró el formulario con ID 'form-" + containerId + "'.");
        }
    } else {
        console.error("No se encontró el botón 'enviar' con el atributo data-form establecido.");
    }
} */


function actualizarEstado(event) {
    const dropdownItem = event.target.closest('.dropdown-item');

    if (dropdownItem) {
        const estadoInput = event.target.closest('.dropdown').querySelector('input[name="estado"]');
        const menuId = event.target.closest('.dropdown').id;

        if (estadoInput) {
            console.log("Se cambio el valor")
            estadoInput.value = dropdownItem.getAttribute("data-estado");
            console.log(estadoInput.value)
        }

        // Aquí puedes realizar acciones adicionales con el ID del menú
        console.log(`Menú desplegable ID: ${menuId}`);
    }
}
