/// <reference path='../_all.ts' />


namespace Mappino.Map {
    'use strict';

    export class MapController {
        private _map: any;

        public static $inject = [
            '$scope',
            '$rootScope',
            'MAP',
            'FiltersService',
            'MarkersService'
        ];

        constructor(private $scope,
                    private $rootScope: any,
                    private MAP: any,
                    private filtersService: FiltersService,
                    private markersService: MarkersService) {
            // ---------------------------------------------------------------------------------------------------------
            this.initMap();

            $scope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', () => markersService.place(this._map));

            $scope.$on('Mappino.Map.PlaceAutocompleteController.PlaceChanged', (event, place) => {
                this.positioningMap(place);
            });
        }



        private initMap() {
            var mapFilters = this.filtersService.filters['map'];

            var mapOptions: google.maps.MapOptions = {
                center:     new google.maps.LatLng(mapFilters['l'].split(',')[0], mapFilters['l'].split(',')[1]),
                zoom:       parseInt(mapFilters['z']),
                mapTypeId:  google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,

                zoomControl: true,
                zoomControlOptions: {
                    position: google.maps.ControlPosition.LEFT_BOTTOM
                },

                mapTypeControl: true,
                mapTypeControlOptions: {
                    position: google.maps.ControlPosition.BOTTOM_LEFT
                },

                styles: this.MAP.STYLES
            };

            this._map = new google.maps.Map(document.getElementById("map"), mapOptions);

            google.maps.event.addListener(this._map, 'idle', () => {
                this.filtersService.update('map', {
                    z: this._map.getZoom(),
                    v: this._map.getBounds(),
                    l: this._map.getCenter().toUrlValue()
                });
                this.$rootScope.mapZoom = this._map.getZoom();
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
