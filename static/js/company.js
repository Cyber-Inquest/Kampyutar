$(".bb_slideshow_content").owlCarousel({
    loop: true,
    autoplay: true,
    autoplayTimeout: 2000, //2000ms = 2s;
    autoplayHoverPause: true,
    items: 1,
    dots:false,
    nav: true,  
});

$(".this_container").owlCarousel({
    loop: false,
    autoplay: true,
    autoplayTimeout: 4000, //2000ms = 2s;
    autoplayHoverPause: true,
    dots:false,
    nav: false,
    margin: 15,
    stagePadding: 0,
    responsive: {
        0: {
            items: 1
        },
        400: {
            items: 2
        },
        600: {
            items: 4.2
        },
        1000: {
            items: 5
        }
    }
});

$(".bb_company_track").owlCarousel({
    loop: true,
    autoplay: true,
    autoplayTimeout: 4000, //2000ms = 2s;
    autoplayHoverPause: true,
    nav: true,
    dots:false,
    margin: 0,
    stagePadding: 0,
    responsive: {
        0: {
            items: 1
        },
        400: {
            items: 2
        },
        600: {
            items: 4.2
        },
        1000: {
            items: 5.2
        }
    }
});

$(".bb_blog_div").owlCarousel({
    dots:false,
    nav: true,
    margin: 30,
    stagePadding: 25,
    responsive: {
        0: {
            items: 1
        },
        400: {
            items: 2
        },
        600: {
            items: 4
        },
        1000: {
            items: 5
        }
    }
});

$(".bb_perProduct_row").owlCarousel({
    loop: false,
    autoplay: true,
    autoplayTimeout: 4000, //2000ms = 2s;
    autoplayHoverPause: true,
    dots:false,
    nav: false,
    margin: 15,
    stagePadding: 0,
    responsive: {
        0: {
            items: 1
        },
        400: {
            items: 2
        },
        600: {
            items: 3.2
        },
        1000: {
            items: 4
        }
    }
});