/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class MapController {
        private _map: any;

        public static $inject = [
            '$scope',
            'MAP',
            'FiltersService',
            'MarkersService'
        ];

        constructor(private $scope,
                    private MAP: any,
                    private filtersService: FiltersService,
                    private markersService: MarkersService) {
            // ---------------------------------------------------------------------------------------------------------
            var self = this;
            google.maps.event.addDomListener(window, "load", () => this.initMap(this));

            $scope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', function() {
                markersService.place(self._map)
            });

            $scope.$on('Mappino.Map.PlaceAutocompleteController.PlaceChanged', function(event, place) {
                self.positioningMap(place);
            })
        }



        private initMap(self) {
            var map_options: google.maps.MapOptions = {
                center:     new google.maps.LatLng(this.filtersService.filters['map']['l'].split(',')[0], this.filtersService.filters['map']['l'].split(',')[1]),
                zoom:       parseInt(this.filtersService.filters['map']['z']),
                //mapTypeId:  google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
                styles: this.MAP.STYLES
            };

            self._map = new google.maps.Map(document.getElementById("map"), map_options);

            google.maps.event.addListener(self._map, 'idle', function() {
                self.filtersService.update('map', {
                    z: self._map.getZoom(),
                    v: self._map.getBounds(),
                    l: self._map.getCenter().toUrlValue()
                });
            });
        }



        private positioningMap(place: any) {
            if (!place.geometry)
                return;

            if (place.geometry.viewport) {
                this._map.fitBounds(place.geometry.viewport);
            } else {
                this._map.panTo(place.geometry.location);
                this._map.setZoom(17);
            }
        }
    }
}
