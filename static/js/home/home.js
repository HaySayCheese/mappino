"use strict";

$(function() {

    var home = {
            type: 0,
            operation: 'sale',
            city: "",
            latLng: "",

            /* якщо true — контрол вводу міста на формі підсвітиться,
             * і з’явиться повідомлення про те, що "місто" є необхідним полем.*/
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


    setCurrentYearToFooter();


    /**
     * dropdown initialize
     **/
    dropdown.selectpicker({
        style: 'btn-default btn-lg'
    });
    cityInput.focus();


    /**
     * За замовчуванням, фонове зображення має бути на всю висоту вікна браузера
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
     * Використовується для заповнення строки пошуку даними з підказок під полем.
     * @param city — строка, яку слід вставити в поле.
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



    function setCurrentYearToFooter() {
        var fy = $('.footer-year');
        fy.text(fy.text() + new Date().getFullYear());
    }
});