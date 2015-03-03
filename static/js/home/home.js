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


    setCurrentYearToFooter();


    /**
     * city dropdown initialize
     **/
    citySelect.selectpicker({
        style: 'btn-default btn-lg'
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
        geocoder.geocode( { 'address': cityAutocomplete.getPlace().formatted_address}, function(results, status) {
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

        geocoder.geocode( { 'address': city }, function(results, status) {
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
                operation_sid = $(".choices input[type='radio']:checked").attr("value");

            !operation_sid ? operation_sid = 0 : null;

            $(".city-empty").hide();
        }
        window.location = window.location.href + "map/#!/?r_type_sid=" + type_sid + "&r_operation_sid=" + operation_sid + "&latLng=" + home.latLng + "&zoom=14";
    });


    function setCurrentYearToFooter() {
        var fy = $('.footer-year');
        fy.text(fy.text() + new Date().getFullYear());
    }
});