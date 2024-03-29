namespace Mappino.Map {
    export function GooglePlaceAutocompleteDirective($rootScope, filtersService): ng.IDirective {
        var autocomplete = null;

        return {
            restrict: 'A',
            require: 'ngModel',

            link: (scope, element, attrs, model: any) => {
                var $element = angular.element(element);

                $element.val(filtersService.filters['map']['c']);
                model.$setViewValue(filtersService.filters['map']['c']);

                autocomplete = new google.maps.places.Autocomplete(<HTMLInputElement>element[0], {
                    componentRestrictions: {
                        country: "ua"
                    }
                });

                google.maps.event.addListener(autocomplete, 'place_changed', () => {
                    filtersService.update('map', {
                        c: autocomplete.getPlace().formatted_address
                    });

                    $rootScope.$broadcast('Mappino.Map.PlaceAutocompleteController.PlaceChanged', autocomplete.getPlace());
                });
            }
        };
    }

    GooglePlaceAutocompleteDirective.$inject = ['$rootScope', 'FiltersService'];
}