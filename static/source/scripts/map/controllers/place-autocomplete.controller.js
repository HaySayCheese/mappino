export class PlaceAutocompleteController {
    constructor($scope, $rootScope, filtersService) {
        var self = this;
        this._autocomplete = null;
        this._autocompleteInput = document.getElementById("place-autocomplete");


        /** Listen events */
        google.maps.event.addDomListener(window, "load", () => this.initAutocomplete(self));

        $scope.$on('pages.map.FiltersService.UpdatedFromUrl', (event, filters) => {
            this._autocompleteInput.value = filters.map.c;
        });
    }



    initAutocomplete(self) {
        self._autocomplete = new google.maps.places.Autocomplete(this._autocompleteInput, {
            componentRestrictions: {
                country: "ua"
            }
        });

        google.maps.event.addListener(self._autocomplete, 'place_changed', function() {
            self.filtersService.update('map', {
                c: self._autocomplete.getPlace().formatted_address
            });

            self.$rootScope.$broadcast('pages.map.PlaceAutocompleteController.PlaceChanged', self._autocomplete.getPlace());
            //
            //if (!self.$scope.$$phase)
            //    self.$scope.$apply();
        });
    }
}

PlaceAutocompleteController.$inject = ['$scope', '$rootScope', 'FiltersService'];