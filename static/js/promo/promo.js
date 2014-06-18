"use strict";

$(document).ready(function() {


    var scrollableBlock = $(document),
        scrollableBlockImage = scrollableBlock.find(".img-holder"),
        headerLinksBlock = scrollableBlock.find(".header-links");

    scrollableBlockImage.imageScroll({
        container: $('.wrapper'),
        touch: Modernizr.touch
    });


    /** Обробник евента скрола контента */
    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop();

        $(".image-caption")
            .css("top", '50%')
            .css("top", '+=' + (scrollTop / 1.5))
            .find("h1")
            .css("opacity", (100 / (scrollTop / 6)) - 3)
            .parent()
            .find("img")
            .css("opacity", (100 / (scrollTop / 6)) - 1.8);


        /** Navbar */
        if (scrollTop > $(window).height() - 70) {
            headerLinksBlock.removeClass("slideOutUp").addClass("slideInDown panel");
        } else if (headerLinksBlock.hasClass("panel") && !headerLinksBlock.hasClass("slideOutUp")) {
                headerLinksBlock
                    .removeClass("slideInDown")
                    .addClass("slideOutUp")

                    .delay(300).queue(function(next) {
                        $(this).removeClass("slideOutUp panel");
                        next();
                    })
                    .addClass("slideInDown")
                    .delay(250).queue(function(next) {
                        $(this).removeClass("slideInDown");

                        next();
                    });

            $("a").removeClass("active");
            window.location.hash = "main";
        }

        /** Markers */
        var sections = $("section"),
            markers = $(".tablet-marker");

        if (scrollTop > sections[0].offsetTop - 150) {

            $.each(markers, function(i, el) {
                setTimeout(function() {
                    $(el).addClass("fadeInDown");
                }, 300 + (i * 300));
            });
        }
    });


    /** Скролимо до секції якщо є хеш в урлі */
    window.location.hash && animateScroll(window.location.hash);


    /** Скролимо до секції по кліку на ссилки */
    headerLinksBlock.find('a').click(function(e) {
        animateScroll($(this).attr("href"));

        e.preventDefault();
    });



    /** Функція яка забезпечує плавний скрол */
    function animateScroll(href) {
        $('html, body').animate({
            scrollTop: href != "#main" ? $(href).offset().top - 69 : 0
        }, 500, function () {
            window.location.hash = href;
        });


        $("a").removeClass("active");
        $("a[href$=" + href +"]").addClass("active");
    }

});