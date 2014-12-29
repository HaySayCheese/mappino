"use strict";

$(document).ready(function() {
    var scrollableBlock = $(document),
        scrollableBlockImage = scrollableBlock.find(".img-holder"),
        mainImage = scrollableBlock.find(".img-holder.main"),
        headerLinksBlock = scrollableBlock.find(".header-links");


    scrollableBlockImage.imageScroll({
        container: $('.wrapper'),
        touch: Modernizr.touch
    });


    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop();

        /* Navigation bar logic */
        if (scrollTop > mainImage.innerHeight() - headerLinksBlock.innerHeight()) {
            headerLinksBlock.removeClass("slideOutUp").addClass("slideInDown panel");

        } else if (headerLinksBlock.hasClass("panel") && !headerLinksBlock.hasClass("slideOutUp")){
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
    });
});