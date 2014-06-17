$(document).ready(function() {


    var scrollableBlock = $(".wrapper"),

        scrollableBlockPart = scrollableBlock.find(".content-block-body"),
        scrollableBlockPartImg = scrollableBlock.find("img");


    scrollableBlockPart.css("margin-top", $(document).height());



    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop(),
            headerLinksBlock = scrollableBlock.find(".header-links");


        headerLinksBlock.css({
            "opacity": (100 / (scrollTop / 2 )) - 1.5,
            "top": 50 + (scrollTop / 2)
        });

        headerLinksBlock.css("opacity") < 0.2 ? headerLinksBlock.css("display", "none") : headerLinksBlock.css("display", "block");

        scrollableBlockPartImg.css({
            "-webkit-transform": "translate(0, " + (scrollTop / 2) + "px)",
                "-ms-transform": "translate(0, " + (scrollTop / 2) + "px)",
                    "transform": "translate(0, " + (scrollTop / 2) + "px)"
        });

        console.log(scrollTop / 3)
    });

});