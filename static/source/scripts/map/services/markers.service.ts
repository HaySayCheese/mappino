/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class MarkersService {
        private _filters_for_load_markers: any;

        private _response_markers: Object = {
            red:    {},
            blue:   {}
        };
        private _markers: Object = {
            red:    {},
            blue:   {}
        };

        public static $inject = [
            '$rootScope',
            '$http',
            '$timeout',
            'PublicationHandler'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $http: angular.IHttpService,
                    private $timeout: angular.ITimeoutService,
                    private publicationHandler: PublicationHandler) {
            // ---------------------------------------------------------------------------------------------------------
            var self = this;

            $rootScope.$on('Mappino.Map.FiltersService.CreatedFormattedFilters', function(event, formatted_filters) {
                self._filters_for_load_markers = formatted_filters;

                self.load();
            });
        }



        private load() {
            var self = this;

            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers)).success(function(response) {
                self.clearResponseMarkersObject();

                self._response_markers = response;
                self.$timeout(() => self.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
            });
        }



        public place(map) {
            console.log(this._markers)
            console.log(this._response_markers)
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {
                            if ((angular.isDefined(this._response_markers[panel]) && angular.isUndefined(this._response_markers[panel][marker])) ||
                                this._markers[panel][marker].params.price != this._response_markers[panel][marker].price) {

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

                                if (angular.isDefined(this._response_markers[panel][marker].price)) {
                                    markerLabelOffsetX = this.calcMarkerLabelOffsetX(this._response_markers[panel][marker].price.length);
                                }

                                console.log(markerLabelOffsetX);


                                this._markers[panel][marker] = new MarkerWithLabel({
                                    position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                    map: map,
                                    icon: '',
                                    params: {
                                        id:     this._response_markers[panel][marker].id,
                                        tid:    this._response_markers[panel][marker].tid,
                                        price:  this._response_markers[panel][marker].price
                                    },
                                    labelContent:
                                        `<div class='custom-marker md-whiteframe-z2'>${this._response_markers[panel][marker].price}</div>` +
                                        `<div class='custom-marker-arrow-down'></div>`,
                                    labelClass: "custom-marker-container",
                                    labelAnchor: new google.maps.Point(markerLabelOffsetX, 32)
                                });

                                this.attachClickEventToMarker(this._markers[panel][marker]);

                                this._markers[panel][marker].setMap(map);
                                console.log('added: ' + this._markers[panel][marker])
                            }

                            console.log(this._markers)
                        }
                    }
                }
            }

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
        }



        private attachClickEventToMarker(marker) {
            google.maps.event.addListener(marker, 'click', () => {
                console.log(`Clicked on marker ${marker.params.tid}:${marker.params.id}`);
                this.publicationHandler.open(`${marker.params.tid}:${marker.params.id}`);
            });
        }



        private calcMarkerLabelOffsetX(labelTextLength: number) {
            var offset = 24;

            switch (labelTextLength) {
                case 4:
                    offset = 24;
                    break;
                case 5:
                    offset = 27;
                    break;
                case 6:
                    offset = 28;
                    break;
                case 7:
                    offset = 30;
                    break;
                case 8:
                    offset = 32;
                    break;
                case 9:
                    offset = 34;
                    break;
                case 10:
                    offset = 36;
                    break;
            }

            return (labelTextLength / 2) + offset;
        }



        private clearResponseMarkersObject() {
            this._response_markers = {
                red:    {},
                blue:   {}
            };
        }
    }
}