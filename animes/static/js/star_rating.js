// Obtiene todos los elementos con la clase 'rating-box'
const ratingBoxes = document.querySelectorAll('.rating-box');

// Itera sobre cada elemento 'rating-box'
ratingBoxes.forEach((ratingBox) => {
    // Obtiene el valor del rating de cada 'rating-box'
    const ratingElement = ratingBox.querySelector('.rating');
    const ratingValue = parseFloat(ratingElement.textContent);

    // Obtiene todas las estrellas dentro de la 'rating-box'
    const stars = ratingBox.querySelectorAll('.gold-star');

    // Itera sobre las estrellas y modifica su contenido según el rating decimal
    stars.forEach((star, index) => {
        const starValue = index + 1;

        // Si el valor de la estrella es menor o igual al rating decimal, muestra una estrella completa
        if (starValue <= ratingValue) {
            star.classList.remove('fas', 'fa-star-half-alt');
            star.classList.add('fas', 'fa-star');
        } else if (starValue - 0.5 <= ratingValue) {
            // Si el valor de la estrella menos 0.5 es menor o igual al rating decimal, muestra media estrella
            star.classList.remove('fas', 'fa-star');
            star.classList.add('fas', 'fa-star-half-alt');
        } else {
            // Si no, muestra una estrella vacía
            star.classList.remove('fas', 'fa-star', 'fas', 'fa-star-half-alt');
            star.classList.add('far', 'fa-star');
        }
    });
});
