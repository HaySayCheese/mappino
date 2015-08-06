/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class MarkersService {
        private _filters_for_load_markers: any;

        private responseSimpleMarkers = {
            blue:   {},
            green:  {}
        };

        private responsePieMarkers = {};

        private simpleMarkers = {
            blue:   {},
            green:  {}
        };

        private pieMarkers = {};

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
            $rootScope.$on('Mappino.Map.PublicationService.PublicationFavorite', (event, markerId) => this.addMarkerToFavorites(markerId));
        }



        private load() {
            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers))
                .then(response => {
                    var responseData = response.data['data'];

                    this.clearResponseMarkers();

                    if (angular.isDefined(responseData)) {
                        if (angular.isDefined(responseData.blue) || angular.isDefined(responseData.green)) {
                            this.clearPieMarkers();
                            this.responseSimpleMarkers = responseData;
                        } else {
                            this.clearSimpleMarkers();
                            this.responsePieMarkers = responseData;
                        }
                    }

                    this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
                }, response => {
                    // error
                });
        }



        public place(map: google.maps.Map) {
            // якщо обєкт з маркерами які прийшли з сервера не пустий
            if (Object.keys(this.responseSimpleMarkers.blue).length || Object.keys(this.responseSimpleMarkers.green).length) {
                this.intersectionSimpleMarkers(map);

                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
                return;
            }

            if (Object.keys(this.responsePieMarkers).length) {
                this.intersectionPieMarkers(map);

                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
            }
        }



        private intersectionSimpleMarkers(map: google.maps.Map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {

                            // Видаляємо маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з одним із кольорів маркерів
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з тілом маркера
                            //  - в обєкті з маркерами який прийшов з сервера ціна маркера відрізняється від ціни існуючого маркера
                            if (angular.isUndefined(this.responseSimpleMarkers[color])
                                || (angular.isDefined(this.responseSimpleMarkers[color]) && angular.isUndefined(this.responseSimpleMarkers[color][latLng]))
                                || this.simpleMarkers[color][latLng].params.price != this.responseSimpleMarkers[color][latLng].price) {

                                this.briefsService.remove(this.simpleMarkers[color][latLng].params.id);

                                console.log('deleted: ' + this.simpleMarkers[color][latLng].params.id);

                                this.simpleMarkers[color][latLng].setMap(null);
                                delete this.simpleMarkers[color][latLng];
                            }
                        }
                    }
                }
            }


            // додаємо нові маркери на карту
            for (var color in this.responseSimpleMarkers) {
                if (this.responseSimpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.responseSimpleMarkers[color]) {
                        if (this.responseSimpleMarkers[color].hasOwnProperty(latLng)) {

                            // Додаємо новий маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера є маркер якого нема у вже існуючих маркерах
                            if (angular.isUndefined(this.simpleMarkers[color][latLng])) {
                                var responseMarker = this.responseSimpleMarkers[color][latLng];

                                this.createSimpleMarker(color, latLng, map, responseMarker);
                            }
                        }
                    }
                }
            }
        }



        private intersectionPieMarkers(map: google.maps.Map) {
            for (var latLng in this.pieMarkers) {
                if (this.pieMarkers.hasOwnProperty(latLng)) {

                    // Видаляємо маркер якщо:
                    //  - в обєкті з маркерами який прийшов з сервера немає обєкта з одним із кольорів маркерів
                    //  - в обєкті з маркерами який прийшов з сервера немає обєкта з тілом маркера
                    //  - в обєкті з маркерами який прийшов з сервера ціна маркера відрізняється від ціни існуючого маркера
                    if (angular.isUndefined(this.responsePieMarkers[latLng])
                            || this.pieMarkers[latLng].params.blue_markers != this.responsePieMarkers[latLng].blue
                            || this.pieMarkers[latLng].params.green_markers != this.responsePieMarkers[latLng].green) {

                        console.log('deleted pie marker: ' + latLng);

                        this.pieMarkers[latLng].setMap(null);
                        delete this.pieMarkers[latLng];
                    }
                }
            }

            // додаємо нові маркери на карту
            for (var latLng in this.responsePieMarkers) {
                if (this.responsePieMarkers.hasOwnProperty(latLng)) {

                    // Додаємо новий маркер якщо:
                    //  - в обєкті з маркерами який прийшов з сервера є маркер якого нема у вже існуючих маркерах
                    if (angular.isUndefined(this.pieMarkers[latLng])) {
                        var responseMarker = this.responsePieMarkers[latLng];

                        this.createPieMarker(latLng, map, responseMarker);
                    }
                }
            }
        }



        private createSimpleMarker(color, latLng, map: google.maps.Map, responseMarker) {
            var markerLabelOffsetX = 35,
                markerLat = latLng.split(':')[0],
                markerLng = latLng.split(':')[1];

            if (angular.isDefined(responseMarker.price)) {
                markerLabelOffsetX = this.calcMarkerLabelOffsetX(responseMarker.price.length);
            }

            this.simpleMarkers[color][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    id:     responseMarker.id,
                    tid:    responseMarker.tid,
                    price:  responseMarker.price
                },
                labelContent:
                `<div class='custom-marker md-whiteframe-z2'>${responseMarker.price}</div>` +
                `<div class='custom-marker-arrow-down'></div>`,
                labelClass: `custom-marker-container -${color}`,
                labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
            });

            if (this._visitedMarkers.indexOf(responseMarker.id) != -1) {
                this.simpleMarkers[color][latLng].labelClass += ' -visited'
            }

            this.simpleMarkers[color][latLng].setMap(map);
            console.log('added: ' + this.simpleMarkers[color][latLng]);

            this.briefsService.add({
                id:             responseMarker.id,
                tid:            responseMarker.tid,
                lat:            markerLat,
                lng:            markerLat,
                price:          responseMarker.price,
                title:          responseMarker.title,
                thumbnail_url:  responseMarker.thumbnail_url
            });

            this.attachClickEventToSimpleMarker(this.simpleMarkers[color][latLng]);
        }



        private createPieMarker(latLng, map, responseMarker) {
            var markerLat = latLng.split(':')[0],
                markerLng = latLng.split(':')[1],

                pieBlueMarkers  = responseMarker.blue   || 0,
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


            this.pieMarkers[latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    count:              pieMarkersCount,
                    blue_markers:       pieBlueMarkers,
                    green_markers:      pieGreenMarkers
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

            this.pieMarkers[latLng].setMap(map);
            console.log('added: ' + this.pieMarkers[latLng]);

            this.attachClickEventToPieMarker(this.pieMarkers[latLng], map);
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

            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                            var marker = this.simpleMarkers[color][latLng];
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

            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                            var marker      = this.simpleMarkers[color][latLng],
                                markerMap   = marker.getMap();

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



        private clearResponseMarkers() {
            this.responseSimpleMarkers = {
                blue:   {},
                green:  {}
            };

            this.responsePieMarkers = {};
        }



        private clearSimpleMarkers() {
            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                            this.briefsService.remove(this.simpleMarkers[color][latLng].params.id);
                            this.simpleMarkers[color][latLng].setMap(null);
                            delete this.simpleMarkers[color][latLng];
                        }
                    }
                }
            }

            this.simpleMarkers = {
                blue:   {},
                green:  {}
            }
        }



        private clearPieMarkers() {
            for (var latLng in this.pieMarkers) {
                if (this.pieMarkers.hasOwnProperty(latLng)) {
                    this.pieMarkers[latLng].setMap(null);
                    delete this.pieMarkers[latLng];
                }
            }

            this.pieMarkers = {};
        }
    }
}