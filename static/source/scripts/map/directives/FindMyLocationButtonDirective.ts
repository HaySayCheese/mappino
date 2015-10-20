namespace Mappino.Map {
    export function FindMyLocationButtonDirective($rootScope, filtersService): ng.IDirective {

        return {
            restrict: 'A',

            link: (scope, element, attrs, model: any) => {
                var $element = angular.element(element);

                $element.addClass('find-my-location-button');

                $element.on('click', () => {
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition((position) => {
                            var location = {
                                lat: position.coords.latitude,
                                lng: position.coords.longitude
                            };

                            $rootScope.$broadcast('Mappino.Map.FindMyLocationButton.Find', location)
                        });
                    } else {
                        console.log('fssgsgsg')
                    }
                });
            }
        };
    }

    FindMyLocationButtonDirective.$inject = ['$rootScope', 'FiltersService'];
}