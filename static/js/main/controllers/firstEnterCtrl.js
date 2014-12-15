'use strict';

app.controller('FirstEnterCtrl', function($scope, $location, $timeout, $rootScope, $anchorScroll) {

    $rootScope.pageTitle = "Добро пожаловать на Mappino";

    /* За замовчуванням, фонове зображенян має бути на всю фонову область. */
    $(window).on('resize', function(){
        $('.img-holder.top').css('height', window.innerHeight + 'px');
    }).resize();


    $scope.$watch(function() {
        return sessionStorage.userName;
    }, function(newValue) {
        $scope.userIsLogin = !_.isUndefined(newValue);
    });

    var cityInput = document.getElementById('home-autocomplete'),
    autocomplete = new google.maps.places.Autocomplete(cityInput, {
        componentRestrictions: {
            country: "ua"
        }
    });

    /* Google autocomplete після вибору міста із запропонованих підказок не оновлює scope,
     * через що на сторінку пошуку подається не повна адреса, а лише її частина,
     * та, яка була введена вручну користувачем, і на яку angular зміг зреагувати по ng-change.
     *
     * Даний код змушує ангулар оновлювати scope кожного разу при виборі нового місця. */
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        $scope.$apply(function(){
            $scope.home.city = autocomplete.getPlace().formatted_address;
        });
    });


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

    $timeout(function() {
        dropdown.selectpicker({
            style: 'btn-default btn-lg'
        });
    }, 500);


    $scope.home = {
        type: 1,
        operation: 0,
        city: "",
        cityRequired: false, // якщо true — контрол вводу міста на формі підсвітиться,
                             // і з’явиться повідомлення про те, що місто є необхідним полем.
        flat: {
            rooms_1_1: false,
            rooms_2_2: false,
            rooms_3_3: false,
            rooms_4_0: false
        }
    };

    /**
     * Використовується для заповнення строки пошуку даними з підказок під полем.
     * @param city — строка, яку слід вставити в поле.
     */
    $scope.fillSearchSuggest = function(city){
        $scope.home.city = city;
    };

    /**
     * Викликається кожного разу при зміні строки вводу міста.
     * Використовується для скидання флагу required після кожної зміни поля,
     * щоб коли користувач починає вводити місто, привести поле в стандартний вигляд,
     * навіть, якщо на попередньому етапі воно було підсвіченим.
     */
    $scope.cityInputChanged = function(){
        $scope.home.cityRequired = false;
    };

    /**
     * Викликається при кліку на кнопку "Искать".
     * Перевіряє чи поле вводу міста не пусте, і, кщо все ок —
     * перекидає користувача на сторінку пошуку.
     */
    $scope.startSearch = function(){
        if (! $scope.home.city){
            $scope.home.cityRequired = true; // контроли будуть підсвічені автоматично.
            return;
        }

        $location.search("r_type_sid", $scope.home.type);
        $location.search("r_operation_sid", $scope.home.operation);
        $location.search("city", $scope.home.city);

        $location.path("/search");

        $rootScope.$emit("first-enter-done");
    };

    /**
     * Використовується для простановки року у футері.
     * @returns {number}
     */
    $scope.currentYear = function(){
        return new Date().getFullYear();
    };

    /**
     * Використовується для переходу по якорям.
     * @param id — id якоря, до якого слід перейти.
     */
    $scope.scrollTo = function(id) {
      $location.hash(id);
      $anchorScroll();
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