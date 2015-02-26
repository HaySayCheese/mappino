"use strict";

$(function() {

    var home = {
            type: 0,
            operation: 'sale',
            city: "",
            latLng: "",

            /* ���� true � ������� ����� ���� �� ���� ����������,
             * � �������� ����������� ��� ��, �� "����" � ���������� �����.*/
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
     * �� �������������, ������ ���������� �� ���� �� ��� ������ ���� ��������
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
     * ��������������� ��� ���������� ������ ������ ������ � ������� �� �����.
     * @param city � ������, ��� ��� �������� � ����.
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
        window.location = "/map";

        e.preventDefault();
    });


    function setCurrentYearToFooter() {
        var fy = $('.footer-year');
        fy.text(fy.text() + new Date().getFullYear());
    }
});