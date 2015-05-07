/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class PlaceAutocompleteController {
        private _autocompleteInput: any;
        private _autocomplete: any;


        public static $inject = [
            '$scope',
            'FiltersService'
        ];

        constructor(private $scope,
                    private filtersService: FiltersService) {
            // -
            this._autocompleteInput = document.getElementById("place-autocomplete");


            /** Listen events */
            google.maps.event.addDomListener(window, "load", () => this.initAutocomplete(this));

            $scope.$on('pages.map.FiltersService.UpdatedFromUrl', (event, filters) => {
                this._autocompleteInput.value = filters['map']['c'];
            });
        }



        private initAutocomplete(self) {
            self._autocomplete = new google.maps.places.Autocomplete(<HTMLInputElement>this._autocompleteInput, {
                componentRestrictions: {
                    country: "ua"
                }
            });

            google.maps.event.addListener(self._autocomplete, 'place_changed', function() {
                self.filtersService.update('map', 'c', self._autocomplete.getPlace().formatted_address);
            });
        }
    }
}