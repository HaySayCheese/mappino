/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MarkersService {
        private _filters_for_load_markers: any;

        private _response_markers: Object = {
            red:    {},
            blue:   {},
            green:  {}
        };
        private _markers: Object = {
            red:    {},
            blue:   {},
            green:  {}
        };

        public static $inject = [
            '$rootScope',
            '$http',
            '$timeout'
        ];

        constructor(
            private $rootScope: angular.IRootScopeService,
            private $http: angular.IHttpService,
            private $timeout: angular.ITimeoutService,
            private slidingPanelsHandler: bModules.Panels.ISlidingPanelsHandler) {
            // -
            var self = this;

            $rootScope.$on('pages.map.FiltersService.CreatedFormattedFilters', function(event, formatted_filters) {
                self._filters_for_load_markers = formatted_filters;

                self.load();
            });
        }



        private load() {
            var self = this;

            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers)).success(function(response) {
                self.clearResponseMarkersObject();

                self._response_markers = response;
                self.$timeout(() => self.$rootScope.$broadcast('pages.map.MarkersService.MarkersIsLoaded'));
            });
        }



        public place(map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {
                            if (!this._response_markers[panel][marker]) {
                                this._markers[panel][marker].setMap(null);
                                console.log('deleted: ' + this._markers[panel][marker]);

                                delete this._markers[panel][marker];
                            }
                            console.log(this._markers)
                        }
                    }
                }
            }


            // додаємо новві маркери на карту
            for (var panel in this._response_markers) {
                if (this._response_markers.hasOwnProperty(panel)) {
                    for (var marker in this._response_markers[panel]) {
                        if (this._response_markers[panel].hasOwnProperty(marker)) {

                            if (!this._markers[panel][marker]) {
                                var markerLabelOffsetX = 35;

                                if (this._response_markers[panel][marker].d1.length >= 9 && this._response_markers[panel][marker].d1.length <= 11)
                                    markerLabelOffsetX = 38;
                                if (this._response_markers[panel][marker].d1.length >= 12 && this._response_markers[panel][marker].d1.length <= 14)
                                    markerLabelOffsetX = 42;

                                console.log(this._response_markers[panel][marker].d1.length)
                                console.log(markerLabelOffsetX)


                                this._markers[panel][marker] = new MarkerWithLabel({
                                    position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                    map: map,
                                    labelContent:
                                        "<div class='custom-marker md-whiteframe-z2'>" + this._response_markers[panel][marker].d1 + "</div>" +
                                        "<div class='custom-marker-arrow-down'></div>",
                                    labelClass: "custom-marker-container",
                                    labelAnchor: new google.maps.Point(markerLabelOffsetX, 32)
                                });
                                this._markers[panel][marker].setMap(map);
                                console.log('added: ' + this._markers[panel][marker])
                            }

                            console.log(this._markers)
                        }
                    }
                }
            }

            this.$timeout(() => this.$rootScope.$broadcast('pages.map.MarkersService.MarkersPlaced'));
        }



        private clearResponseMarkersObject() {
            this._response_markers = {
                red:    {},
                blue:   {},
                green:  {}
            };
        }
    }
}