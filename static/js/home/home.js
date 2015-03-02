"use strict";

$(function() {

    var home = {
            type: 0,
            operation: 0,
            city: "",
            latLng: "",

            /* пїЅпїЅпїЅпїЅ true пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ,
             * пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅ, пїЅпїЅ "пїЅпїЅпїЅпїЅ" пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅ.*/
            cityRequired: false
        },
        cityInput = document.getElementById('home-location-autocomplete'),
        dropdown = $(".type-selectpicker"),
        first_enter_autocomplete = new google.maps.places.Autocomplete(cityInput, {
            componentRestrictions: {
                country: "ua"
            }
        }),
        geocoder = new google.maps.Geocoder();

    $(document).find(".img-holder").imageScroll({
        container: $('.wrapper'),
        touch: Modernizr.touch
    });


    setCurrentYearToFooter();


    /**
     * dropdown initialize
     **/
    dropdown.selectpicker({
        style: 'btn-default btn-lg'
    });
    cityInput.focus();
    $(".city-empty").hide();


    /**
     * пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ, пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
     **/
    $(window).on('resize', function() {
        $('.img-holder.top').css('height', $(window).height() + 'px');
    }).resize();

    $(cityInput).change(function(e) {
        if (e.currentTarget.value) {
            $(".city-empty").hide();
        } else {
            $(".city-empty").show();
        }

    });



    /**
     * autocomplete 'place_changed' event handler
     **/
    google.maps.event.addListener(first_enter_autocomplete, 'place_changed', function() {
        geocoder.geocode( { 'address': first_enter_autocomplete.getPlace().formatted_address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK)
                home.latLng = results[0].geometry.location.lat() + "," + results[0].geometry.location.lng();
        });

        home.city = first_enter_autocomplete.getPlace().formatted_address;
    });


    /**
     * пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅ.
     * @param city пїЅ пїЅпїЅпїЅпїЅпїЅпїЅ, пїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅ.
     */
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