$(document).ready(function () {
    let currentSlide = 0;
    const slides = $('.slider-image');

    function showSlide(index) {
        slides.removeClass('active').eq(index).addClass('active');
    }

    showSlide(currentSlide);

    $('.left-control').click(function () {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    });

    $('.right-control').click(function () {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    });

    // Добавление в корзину
    $('.add-to-cart-btn').click(function (e) {
        e.preventDefault();
        alert('Датасет добавлен в корзину');
        // Добавьте ваш код для добавления датасета в корзину
    });
});