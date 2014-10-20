'use strict';

app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope) {

    $rootScope.pageTitle = "Добро пожаловать на Mappino";
    $scope.firstEnter = {
        city: $location.search().city || "",
        latLng: ""
    };

    $scope.$watch(function() {
        return sessionStorage.userName;
    }, function(newValue) {
        $scope.userIsLogin = !_.isUndefined(newValue);
    });

    var input = document.getElementById('first-enter-autocomplete');

    var firstEnterModal = angular.element(".first-enter-modal");
    firstEnterModal.modal();


    ga('send', 'pageview', {
        'page': '#!/first-enter',
        'title': $rootScope.pageTitle
    });


    var scrollableBlock = $(".modal-content"),
        dropdown        = $(".type-selectpicker"),
        scrollableBlockImage = $(".img-holder"),
        headerLinksBlock = scrollableBlock.find(".header-links");

    dropdown.selectpicker({
        style: 'btn-default btn-lg'
    });


    $scope.home = {
        operation: "sale",
        flat: {
            rooms_1_1: false,
            rooms_2_2: false,
            rooms_3_3: false,
            rooms_4_0: false
        }
    };


    $scope.isYo = function(obj, positives) {
        var _obj = $scope.home[obj],
            _objLength = 0,
            pos_count = 0,
            neg_count = 0;

        // Calc positve checkbox checked
        for (var a = 0; a <= positives.length; a++) {
            for (var p in _obj) {
                if (_obj.hasOwnProperty(p) && p == positives[a] && _obj[p])
                    pos_count++;
            }
        }

        // Calc negative checkbox checked
        for (var n in _obj) {
            if (_obj.hasOwnProperty(n)) {
                if (!positives[1] && n != positives[0] && !_obj[n])
                    neg_count++;
                else if (positives[1] && n != positives[1] && !_obj[n])
                    neg_count++;
            }

            _objLength++;
        }

        // If alles gute return true )
        if (pos_count == positives.length && neg_count == (_objLength - positives.length))
            return true;
    };


    /** Обробник евента скрола контента */
    scrollableBlock.scroll(function() {
        var scrollTop = scrollableBlock.scrollTop();

        setTimeout(function() {
            $(".image-caption")
                .find("h1")
                .css("opacity", (100 / (scrollTop / 7)) - 1.2)
                .parent()
                .find("img")
                .css("opacity", (100 / (scrollTop / 9)) - 2);
        }, 100);



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



    function firstEnterDone() {
        $location.path("/search");
    }

});