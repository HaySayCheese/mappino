namespace Mappino.Map {
    export function FindMyLocationButtonDirective(filtersService): ng.IDirective {

        return {
            restrict: 'A',

            link: (scope, element, attrs, model: any) => {
                var $element = angular.element(element);

                $element.addClass('find-my-location-button');

                $element.on('click', () => {
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition((position) => {
                            var lat = position.coords.latitude,
                                lng = position.coords.longitude;

                                filtersService.update('map', {
                                    l: new google.maps.LatLng(lat, lng).toUrlValue(),
                                    z: 15
                                });
                        });
                    } else {
                        console.log('fssgsgsg')
                    }
                });
            }
        };
    }

    FindMyLocationButtonDirective.$inject = ['FiltersService'];
}