$(".v_tB_brandSlideShow").owlCarousel({
    loop: false,
    autoplay: false,
    autoplayTimeout: 4000, //2000ms = 2s;
    autoplayHoverPause: true,
    dots:false,
    nav: false,
    margin: 15,
    stagePadding: 0,
    responsive: {
        0: {
            items: 3
        },
        400: {
            items: 4
        },
        600: {
            items: 7
        },
        800: {
            items: 10
        },
        1000: {
            items: 14
        }
    }
});