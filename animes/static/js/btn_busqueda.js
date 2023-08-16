const botonBusquedaMenor = document.getElementById('botonBusquedaMenor');
const inputBusqueda = document.getElementById('inputBusqueda');
const botonesBusqueda = document.querySelectorAll('.busqueda');
const busqueda = document.getElementById('busqueda');
const logo = document.getElementById('logo');

let busquedaMenorVisible = false;

botonBusquedaMenor.addEventListener('click', (event) => {
    event.preventDefault(); // Evitar que se recargue la página

    busquedaMenorVisible = !busquedaMenorVisible;
    
    if (busquedaMenorVisible) {
        inputBusqueda.style.display = 'none';
        botonesBusqueda.forEach(boton => boton.style.display = 'inline-block');
        busqueda.style.display = 'inline-block';
        logo.style.display = 'none';
        botonBusquedaMenor.innerHTML = '<span class="fa-solid fa-xmark"></span>';
        botonBusquedaMenor.classList.replace('btn-success', 'btn-danger'); // Modificar clase
    } else {
        inputBusqueda.style.display = 'inline-block';
        botonesBusqueda.forEach(boton => boton.style.display = 'none');
        logo.style.display = 'block';
        busqueda.style.display = 'none';
        botonBusquedaMenor.innerHTML = '<span class="fa-solid fa-magnifying-glass"></span>';
        botonBusquedaMenor.classList.replace('btn-danger', 'btn-success'); // Quitar clase  
    }
});

