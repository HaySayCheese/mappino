/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class MarkersService {
        private _filters_for_load_markers: any;

        private _response_markers: Object = {
            blue:   {},
            green:  {}
        };
        private _markers: Object = {
            blue:   {},
            green:  {}
        };

        private _visitedMarkers = [];

        public static $inject = [
            '$rootScope',
            '$http',
            '$timeout',
            'PublicationHandler',
            'BriefsService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $http: angular.IHttpService,
                    private $timeout: angular.ITimeoutService,
                    private publicationHandler: PublicationHandler,
                    private briefsService: BriefsService) {
            // ---------------------------------------------------------------------------------------------------------
            var self = this;

            this.parseVisitedMarkers();
            this.parseFavoritesMarkers();

            $rootScope.$on('Mappino.Map.FiltersService.CreatedFormattedFilters', function(event, formatted_filters) {
                self._filters_for_load_markers = formatted_filters;

                self.load();
            });

            $rootScope.$on('Mappino.Map.BriefsService.BriefMouseOver', (event, markerId) => this.highlightMarker(markerId, 'hover'));
            $rootScope.$on('Mappino.Map.BriefsService.BriefMouseLeave', event => this.clearHighlight());
            $rootScope.$on('Mappino.Map.PublicationService.PublicationVisited', (event, markerId) => {
                this.highlightMarker(markerId, 'visited');
                this.addMarkerToVisited(markerId);
            });
            $rootScope.$on('Mappino.Map.PublicationService.PublicationFavorite', (event, markerId) => {
                //this.highlightMarker(markerId, 'visited');
                this.addMarkerToFavorites(markerId);
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

                                this.briefsService.remove(this._markers[panel][marker].params.id);

                                this._markers[panel][marker].setMap(null);
                                delete this._markers[panel][marker];

                                console.log('deleted: ' + this._markers[panel][marker]);
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
                                var markerLabelOffsetX = 35,
                                    _responseMarker = this._response_markers[panel][marker];

                                if (angular.isDefined(_responseMarker.price)) {
                                    markerLabelOffsetX = this.calcMarkerLabelOffsetX(_responseMarker.price.length);
                                }

                                this._markers[panel][marker] = new MarkerWithLabel({
                                    position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                    map: map,
                                    icon: '../mappino_static/build/images/markers/empty_marker.png',
                                    params: {
                                        id:     _responseMarker.id,
                                        tid:    _responseMarker.tid,
                                        price:  _responseMarker.price
                                    },
                                    labelContent:
                                        `<div class='custom-marker md-whiteframe-z2'>${_responseMarker.price}</div>` +
                                        `<div class='custom-marker-arrow-down'></div>`,
                                    labelClass: `custom-marker-container -${panel}`,
                                    labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
                                });

                                if (this._visitedMarkers.indexOf(_responseMarker.id) != -1) {
                                    this._markers[panel][marker].labelClass += ' -visited'
                                }

                                this.attachClickEventToMarker(this._markers[panel][marker]);

                                this.briefsService.add({
                                    id: _responseMarker.id,
                                    tid: _responseMarker.tid,
                                    price: _responseMarker.price,
                                    title: _responseMarker.title,
                                    thumbnail_url: _responseMarker.thumbnail_url
                                });

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
                case 11:
                    offset = 39;
                    break;
            }

            return (labelTextLength / 2) + offset;
        }



        private highlightMarker(markerId: string, action: string) {
            var ACTION_CLASS = null;

            switch (action) {
                case 'hover':
                    ACTION_CLASS = '-hover';
                    break;
                case 'visited':
                    ACTION_CLASS = '-visited';
                    break;
            }

            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {
                            var marker = this._markers[panel][marker];
                            var markerMap = marker.getMap();

                            if (marker.params.id == markerId && marker.labelClass.indexOf(ACTION_CLASS) == -1) {
                                marker.labelClass += ` ${ACTION_CLASS}`;
                                marker.setMap(null);
                                marker.setMap(markerMap);
                            }
                        }
                    }
                }
            }
        }



        private clearHighlight() {
            var HOVER_CLASS = '-hover';

            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {
                            var marker = this._markers[panel][marker];
                            var markerMap = marker.getMap();

                            if (marker.labelClass.indexOf(HOVER_CLASS) != -1) {
                                marker.labelClass = marker.labelClass.substring(0, marker.labelClass.indexOf(HOVER_CLASS));
                                marker.setMap(null);
                                marker.setMap(markerMap)
                            }
                        }
                    }
                }
            }
        }



        private addMarkerToVisited(markersId: string) {
            var visited = [];

            if (sessionStorage) {
                if (sessionStorage.getItem('visitedMarkers')) {
                    visited.push(sessionStorage.getItem('visitedMarkers').split());
                }

                if (visited.join().indexOf(markersId) == -1) {
                    visited.push(markersId);
                    sessionStorage.setItem('visitedMarkers', visited.join());
                }
            }
        }


        private parseVisitedMarkers() {
            if (sessionStorage && sessionStorage.getItem('visitedMarkers')) {
                this._visitedMarkers = sessionStorage.getItem('visitedMarkers');
            }
        }



        private addMarkerToFavorites(markersId: string) {
            var favorites = [];

            if (sessionStorage) {
                if (sessionStorage.getItem('favoritesMarkers')) {
                    favorites.push(sessionStorage.getItem('favoritesMarkers').split());
                }

                if (favorites.join().indexOf(markersId) == -1) {
                    favorites.push(markersId);
                    sessionStorage.setItem('favoritesMarkers', favorites.join());
                }
            }
        }


        private parseFavoritesMarkers() {
            if (sessionStorage && sessionStorage.getItem('favoritesMarkers')) {
                this._visitedMarkers = sessionStorage.getItem('favoritesMarkers');
            }
        }



        private clearResponseMarkersObject() {
            this._response_markers = {
                blue:   {},
                green:  {}
            };
        }
    }
}