"use strict";


$(function() {

    var home = {
            city: "",
            latLng: "",
            cityRequired: false
        },
        cityIsEmptyMessageText = $(".city-empty").hide(),
        cityInput = document.getElementById('home-location-autocomplete'),
        citySelect = $(".type-selectpicker"),
        cityAutocomplete = new google.maps.places.Autocomplete(cityInput, {
            componentRestrictions: {
                country: "ua"
            }
        }),
        geocoder = new google.maps.Geocoder();


    /**
     * Init 'imageScroll' parallax plugin
     **/
    $(document).find(".img-holder").imageScroll({
        container: $('.wrapper'),
        touch: Modernizr.touch
    });


    placeMarkers();
    setCurrentYearToFooter();


    /**
     * city dropdown initialize
     **/
    citySelect.selectpicker({
        style: 'btn-default btn-lg'
    }).on("change", function() {
        var dailyBtn = $(".choices .btn input[value='2']").parent();

        this.value > 2 ?
            dailyBtn.attr("disabled", true) :
            dailyBtn.attr("disabled", false) ;
    });
    cityInput.focus();


    /**
     * set '$('.img-holder.top')' div to height of window if he is resize
     **/
    $(window).on('resize', function() {
        $('.img-holder.top').css('height', $(window).height() + 'px');
    }).resize();


    /**
     * show/hide message when city input is null
     **/
    $(cityInput).change(function(e) {
        e.currentTarget.value ? cityIsEmptyMessageText.hide() : cityIsEmptyMessageText.show();
    });


    /**
     * autocomplete 'place_changed' event handler
     **/
    google.maps.event.addListener(cityAutocomplete, 'place_changed', function() {
        geocoder.geocode({
            'address': cityAutocomplete.getPlace().formatted_address
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK)
                home.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
        });

        home.city = cityAutocomplete.getPlace().formatted_address;
    });


    /**
     * city suggests handler
     **/
    $("[data-suggest]").click(function(e) {
        var city = $(e.currentTarget).data("suggest");
        home.city = city;
        $(cityInput).val(city).change();

        geocoder.geocode({
            'address': city
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK)
                home.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
        });

        e.preventDefault();
    });


    /**
     * search button click handler
     **/
    $("[data-search-btn]").click(function(e) {
        //window.location = "/map";

        if (!home.latLng) {
            $(".city-empty").show();
            e.preventDefault();
            return;
        } else {
            var type_sid = $(".type-selectpicker").val(),
                operation_sid = $(".choices input[type='radio']:checked").attr("value"),
                period_sid = null;

            !operation_sid ? operation_sid = 0 : null;

            if (operation_sid == 2) {
                operation_sid = 1;
                period_sid = 1;
            }


            $(".city-empty").hide();
        }
        window.location =
            window.location.href +
            "map/#!/?city=" + home.city +
            "&r_type_sid=" + type_sid +
            "&r_operation_sid=" + operation_sid +
            "&latLng=" + home.latLng +
            "&zoom=14" +
            (period_sid ? "&r_period_sid=" + period_sid : "");
    });


    $("[data-scroll-top]").on('click', function() {
        $("html, body").animate({
            scrollTop:0
        }, '500');
        return false;
    });



    function placeMarkers() {
        var sections = $("section"),
            markers = $(".tablet-marker"),
            scrollTop = 0;

        $(document).scroll(function() {
            scrollTop = $(document).scrollTop();


            if (scrollTop > sections[2].offsetTop - 150) {
                $.each(markers, function(i, el) {
                    setTimeout(function() {
                        $(el).addClass("fadeInDown");
                    }, 300 + (i * 300));
                });
            }
        });


    }


    function setCurrentYearToFooter() {
        var fy = $('.footer-year');
        fy.text(fy.text() + new Date().getFullYear());
    }
});
