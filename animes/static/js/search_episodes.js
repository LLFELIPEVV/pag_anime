document.addEventListener('DOMContentLoaded', function () {
    const orderSelect = document.getElementById('order');
    const episodeSearch = document.getElementById('episode-search');
    const animeItems = document.querySelectorAll('.anime-item');

    // Función para ordenar los elementos
    function sortItems(order) {
        const animeList = document.querySelector('.anime-list');
        const items = Array.from(animeList.getElementsByClassName('anime-item'));
        items.sort(function (a, b) {
            const episodeA = parseInt(a.getAttribute('data-capitulo-lista'));
            const episodeB = parseInt(b.getAttribute('data-capitulo-lista'));
            return (order === 'asc') ? episodeA - episodeB : episodeB - episodeA;
        });
        items.forEach(function (item) {
            animeList.appendChild(item);
        });
    }

    // Evento para cambiar el orden
    orderSelect.addEventListener('change', function () {
        const order = orderSelect.value;
        sortItems(order);
    });

    // Función para realizar la búsqueda
    function searchItems(query) {
        animeItems.forEach(function (item) {
            const episodeNumber = item.getAttribute('data-capitulo-lista');
            if (episodeNumber.includes(query)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Evento para la barra de búsqueda
    episodeSearch.addEventListener('input', function () {
        const searchQuery = episodeSearch.value.toLowerCase();
        searchItems(searchQuery);
    });

    // Inicialmente, ordena los elementos en orden ascendente
    sortItems('asc');
});
