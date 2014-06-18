$(document).ready(function() {


    var scrollableBlock = $(document),
        scrollableBlockImage = scrollableBlock.find(".img-holder"),
        headerLinksBlock = scrollableBlock.find(".header-links");

    scrollableBlockImage.imageScroll({
        container: $('.wrapper')
    });


    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop();

        $(".image-caption")
            .css("top", '50%')
            .css("top", '+=' + (scrollTop / 1.5))
            .find("h1")
            .css("opacity", (100 / (scrollTop / 6)) - 2)
            .parent()
            .find("img")
            .css("opacity", (100 / (scrollTop / 6)) - 1);


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

        if (scrollTop > sections[0].offsetTop - 100) {

            $.each(markers, function(i, el) {
//                $(el).addClass("fadeInDown");

                setTimeout(function() {
                    $(el).addClass("fadeInDown");
                }, 300 + (i * 300));
            });


//            for (var i = 0; i <= markers.length; i++) {
//                $(".tablet-marker.m-" + i)
//                    //.addClass("fadeInDown")
//                    .delay(250).queue(function(next) {
//                        $(this).addClass("fadeInDown");
//
//                        next();
//                    });
//            }
        }
    });

});