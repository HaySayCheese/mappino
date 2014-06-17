$(document).ready(function() {


    var scrollableBlock = $(document),
        scrollableBlockImage = scrollableBlock.find(".img-holder"),
        headerLinksBlock = scrollableBlock.find(".header-links");

    scrollableBlockImage.imageScroll({
        container: $('.wrapper'),
        mediaHeight: 1080
    });


    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop();

        $(".image-caption")
            .css("opacity", (100 / (scrollTop / 6)) - 1)
            .css("top", '50%')
            .css("top", '+=' + (scrollTop / 1.5));

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
    });

});