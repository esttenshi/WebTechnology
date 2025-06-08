$(document).ready(function(){
    var carousel = $('#carouselExampleIndicators');
    var totalItems = $('.carousel-item').length;
    var currentIndex = 0;
    var isAnimating = false;

    function nextSlide() {
        if (!isAnimating) {
            isAnimating = true;
            currentIndex = (currentIndex + 1) % totalItems;
            carousel.carousel(currentIndex);
        }
    }

    var interval = setInterval(nextSlide, 5000);

    carousel.on('mouseenter', function() {
        clearInterval(interval);
    });

    carousel.on('mouseleave', function() {
        interval = setInterval(nextSlide, 3000);
    });

    carousel.on('slid.bs.carousel', function () {
        isAnimating = false;
    });
});

$(document).ready(function(){
    $("#photoCarousel .carousel-control-prev").click(function(event){
        event.preventDefault();
        $("#photoCarousel").carousel("prev");
    });

    $("#photoCarousel .carousel-control-next").click(function(event){
        event.preventDefault();
        $("#photoCarousel").carousel("next");
    });
});




