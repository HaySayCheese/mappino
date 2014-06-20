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

});