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

            $scope.$on('pages.map.MarkersService.MarkersDone', function() {
                markersService.place(self._map)
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
                self.filtersService.update('map', 'z', self._map.getZoom());
                self.filtersService.update('map', 'v', self._map.getBounds());
                self.filtersService.update('map', 'l', self._map.getCenter().toUrlValue());
            });
        }
    }
}
