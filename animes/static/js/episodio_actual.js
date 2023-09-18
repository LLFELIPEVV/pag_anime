//Selecciona el capitulo en el que se esta actualmente
document.addEventListener('DOMContentLoaded', function () {
    var capituloActualElemento = document.querySelector('p[data-capitulo-actual]');
    
    if (capituloActualElemento) {
        var capituloActual = capituloActualElemento.dataset.capituloActual;
        
        var numeroEpisodio = document.querySelectorAll('li[data-capitulo-lista]');
        
        numeroEpisodio.forEach(function (numero) {
            var data_episodio = numero.dataset.capituloLista;
            console.log(data_episodio)
            
            if (data_episodio === capituloActual) {
                numero.classList.add('active'); // Agrega la clase 'active' al capítulo actual
            }
        });
    } else {
        console.log("El elemento 'p[data-capitulo-actual]' no fue encontrado.");
    }
});

