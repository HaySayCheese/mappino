/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class PlaceAutocompleteController {
        private _autocompleteInput: any;
        private _autocomplete: any;


        public static $inject = [
            '$scope',
            '$rootScope',
            'FiltersService'
        ];

        constructor(private $scope,
                    private $rootScope: angular.IRootScopeService,
                    private filtersService: FiltersService) {
            // ---------------------------------------------------------------------------------------------------------
            var self = this;
            this._autocompleteInput = document.getElementById("place-autocomplete");


            /** Listen events */
            google.maps.event.addDomListener(window, "load", () => this.initAutocomplete(self));

            $scope.$on('Mappino.Map.FiltersService.UpdatedFromUrl', (event, filters) => {
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
                self.filtersService.update('map', {
                    c: self._autocomplete.getPlace().formatted_address
                });

                self.$rootScope.$broadcast('Mappino.Map.PlaceAutocompleteController.PlaceChanged', self._autocomplete.getPlace());
                //
                //if (!self.$scope.$$phase)
                //    self.$scope.$apply();
            });
        }
    }
}