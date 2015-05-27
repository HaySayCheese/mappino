/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MapController {
        private _map: any;

        public static $inject = [
            '$scope',
            'FiltersService',
            'MarkersService'
        ];

        constructor(private $scope,
                    private filtersService: FiltersService,
                    private markersService: MarkersService) {
            // -
            var self = this;
            google.maps.event.addDomListener(window, "load", () => this.initMap(this));

            $scope.$on('pages.map.MarkersService.MarkersIsLoaded', function() {
                markersService.place(self._map)
            });

            $scope.$on('pages.map.PlaceAutocompleteController.PlaceChanged', function(event, place) {
                self.positioningMap(place);
            })
        }



        private initMap(self) {
            self._map = new google.maps.Map(document.getElementById("map"), {
                center:     new google.maps.LatLng(this.filtersService.filters['map']['l'].split(',')[0], this.filtersService.filters['map']['l'].split(',')[1]),
                zoom:       parseInt(this.filtersService.filters['map']['z']),
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true
            });

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
