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
            this.parseVisitedMarkers();
            this.parseFavoritesMarkers();

            $rootScope.$on('Mappino.Map.FiltersService.CreatedFormattedFilters', (event, formatted_filters) => {
                this._filters_for_load_markers = formatted_filters;

                this.load();
            });

            $rootScope.$on('Mappino.Map.BriefsService.BriefMouseOver', (event, markerId) => this.highlightMarker(markerId, 'hover'));
            $rootScope.$on('Mappino.Map.BriefsService.BriefMouseLeave', event => this.clearHighlight());
            $rootScope.$on('Mappino.Map.PublicationService.PublicationVisited', (event, markerId) => {
                this.highlightMarker(markerId, 'visited');
                this.addMarkerToVisited(markerId);
            });
            $rootScope.$on('Mappino.Map.PublicationService.PublicationFavorite', (event, markerId) => {
                this.addMarkerToFavorites(markerId);
            });
        }



        private load() {
            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers))
                .then(response => {
                    this.clearResponseMarkersObject();

                    this._response_markers = response.data;
                    this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
                }, response => {

                });
        }



        public place(map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var panel in this._markers) {
                if (this._markers.hasOwnProperty(panel)) {
                    for (var marker in this._markers[panel]) {
                        if (this._markers[panel].hasOwnProperty(marker)) {

                            if (angular.isUndefined(this._response_markers[panel]) ||
                                (angular.isDefined(this._response_markers[panel]) && angular.isUndefined(this._response_markers[panel][marker])) ||
                                this._markers[panel][marker].params.price != this._response_markers[panel][marker].price) {

                                this.briefsService.remove(this._markers[panel][marker].params.id);

                                console.log('deleted: ' + this._markers[panel][marker].params.id);

                                this._markers[panel][marker].setMap(null);
                                delete this._markers[panel][marker];
                            }
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
                                var responseMarker = this._response_markers[panel][marker];

                                if (responseMarker.price) {
                                    this.createSimpleMarker(panel, marker, map, responseMarker);
                                } else {
                                    this.createPieMarker(panel, marker, map, responseMarker);
                                }
                            }
                        }
                    }
                }
            }

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
        }



        private createSimpleMarker(panel, marker, map, responseMarker) {
            var markerLabelOffsetX = 35;

            if (angular.isDefined(responseMarker.price)) {
                markerLabelOffsetX = this.calcMarkerLabelOffsetX(responseMarker.price.length);
            }

            this._markers[panel][marker] = new MarkerWithLabel({
                position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                //map: map,
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    id:     responseMarker.id,
                    tid:    responseMarker.tid,
                    price:  responseMarker.price
                },
                labelContent:
                `<div class='custom-marker md-whiteframe-z2'>${responseMarker.price}</div>` +
                `<div class='custom-marker-arrow-down'></div>`,
                labelClass: `custom-marker-container -${panel}`,
                labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
            });

            if (this._visitedMarkers.indexOf(responseMarker.id) != -1) {
                this._markers[panel][marker].labelClass += ' -visited'
            }

            this._markers[panel][marker].setMap(map);
            console.log('added: ' + this._markers[panel][marker]);

            this.briefsService.add({
                id:             responseMarker.id,
                tid:            responseMarker.tid,
                price:          responseMarker.price,
                title:          responseMarker.title,
                thumbnail_url:  responseMarker.thumbnail_url
            });

            this.attachClickEventToSimpleMarker(this._markers[panel][marker]);
        }



        private createPieMarker(panel, marker, map, responseMarker) {
            var pieBlueMarkers  = responseMarker.blue   || 0,
                pieGreenMarkers = responseMarker.green  || 0,

                pieMarkersCount = pieBlueMarkers + pieGreenMarkers,

                pieBlueMarkersCountInDeg    = Math.round((360 / 100 * ((pieBlueMarkers / pieMarkersCount) * 100))   || 0),
                pieGreenMarkersCountInDeg   = Math.round((360 / 100 * ((pieGreenMarkers / pieMarkersCount) * 100))  || 0),

                blueAdditionalClass      = pieBlueMarkersCountInDeg  > 180 ? ' full' : '',
                greenAdditionalClass     = pieGreenMarkersCountInDeg > 180 ? ' full' : '',

                sizeOfPieChart = pieMarkersCount < 100 ? "small" :
                    pieMarkersCount >= 100 && pieMarkersCount < 1000 ? "medium" :
                        pieMarkersCount >= 1000 && pieMarkersCount < 10000 ? "large" : "super-big",

                _uuid = _.uniqueId('pie-marker-');


            this._markers[panel][marker] = new MarkerWithLabel({
                position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    count:             pieMarkersCount,
                    bluePercentage:    pieBlueMarkers,
                    greenPercentage:   pieGreenMarkers
                },
                labelContent:
                    "<style>" +
                        "." + _uuid + ".pie.pie-blue {" +
                            "transform: rotate(0deg);" +
                        "}"+
                        "." + _uuid + ".pie.pie-blue:before {" +
                            "transform: rotate(" + pieBlueMarkersCountInDeg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.pie-green {" +
                            "transform: rotate(" + pieBlueMarkersCountInDeg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.pie-green:before {" +
                            "transform: rotate(" + pieGreenMarkersCountInDeg + "deg);" +
                        "}"+
                    "</style>"+
                    "<div>" +
                        "<div class='marker-pie-chart-inner'>" + pieMarkersCount + "</div>" +
                        "<div class='" + _uuid + " pie pie-blue" + blueAdditionalClass + "'></div>" +
                        "<div class='" + _uuid + " pie pie-green" + greenAdditionalClass + "'></div>" +
                    "</div>",
                labelClass: `marker-pie-chart ${sizeOfPieChart} md-whiteframe-z2`,
                labelAnchor: new google.maps.Point(30, 45),
            });

            this._markers[panel][marker].setMap(map);
            console.log('added: ' + this._markers[panel][marker]);

            this.attachClickEventToPieMarker(this._markers[panel][marker], map);
        }



        private attachClickEventToPieMarker(marker, map) {
            google.maps.event.addListener(marker, 'click', () => {
                map.setZoom(map.getZoom() + 1);
            });
        }



        private attachClickEventToSimpleMarker(marker) {
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