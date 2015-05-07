/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class PlaceAutocompleteController {
        autocomplete: any;

        public static $inject = [
            '$scope',
            'FiltersService'
        ];

        constructor(private $scope, private filtersService: FiltersService) {
            google.maps.event.addDomListener(window, "load", () => this.initAutocomplete());
        }



        private initAutocomplete() {
            var self = this;

            this.autocomplete = new google.maps.places.Autocomplete(<HTMLInputElement>document.getElementById("place-autocomplete"), {
                componentRestrictions: {
                    country: "ua"
                }
            });

            google.maps.event.addListener(this.autocomplete, 'place_changed', function() {
                console.log('change')
                self.filtersService.mapp({ c: self.autocomplete.getPlace().formatted_address });
            });
        }
    }
}