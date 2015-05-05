app.controller('OfferController', ['$timeout',
    function($timeout) {
        "use strict";

        var scrollableBlock     = $(document),
            imgHolder           = scrollableBlock.find(".img-holder"),
            mainImage           = scrollableBlock.find(".img-holder.main"),
            headerLinksBlock    = scrollableBlock.find(".header-links"),
            accordeons          = $('.toggle-group');


        initPlugins();
        initNavbar();



        var showInterval;
        accordeons.on('show.bs.collapse', function () {
            showInterval = setInterval(function() {
                imgHolder.imageScroll('refresh');
            }, 0);
        });
        accordeons.on('shown.bs.collapse', function () {
            clearInterval(showInterval);
        });

        var hideInterval;
        accordeons.on('hide.bs.collapse', function () {
            hideInterval = setInterval(function() {
                imgHolder.imageScroll('refresh');
            }, 0);
        });
        accordeons.on('hidden.bs.collapse', function () {
            clearInterval(hideInterval);
        });


        function initPlugins() {
            $timeout(function() {
                imgHolder.imageScroll({
                    container: $('.wrapper'),
                    touch: Modernizr.touch
                });
            });
        }

        function initNavbar() {
            scrollableBlock.scroll(function() {
                var scrollTop = scrollableBlock.scrollTop();

                /* Navigation bar logic */
                if (scrollTop > mainImage.innerHeight() - headerLinksBlock.innerHeight()) {
                    headerLinksBlock.removeClass("slideOutUp").addClass("slideInDown toggle");

                } else if (headerLinksBlock.hasClass("toggle") && !headerLinksBlock.hasClass("slideOutUp")){
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
        }
    }
]);