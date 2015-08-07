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

        private favoritesMarkers = {};

        private favoritesPlaced: boolean = false;

        private _visitedMarkers = [];

        public static $inject = [
            '$rootScope',
            '$state',
            '$http',
            '$timeout',
            'PublicationHandler',
            'BriefsService',
            'FavoritesService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $state: angular.ui.IStateService,
                    private $http: angular.IHttpService,
                    private $timeout: angular.ITimeoutService,
                    private publicationHandler: PublicationHandler,
                    private briefsService: BriefsService,
                    private favoritesService: FavoritesService) {
            // ---------------------------------------------------------------------------------------------------------
            this.parseVisitedMarkers();
            this.parseFavoritesMarkers();

            $rootScope.$on('Mappino.Map.FiltersService.CreatedFormattedFilters', (event, formatted_filters) => {
                this._filters_for_load_markers = formatted_filters;
                this.load();
            });

            $rootScope.$on('Mappino.Map.FavoritesService.FavoritesIsLoaded', event => {
                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
            });

            $rootScope.$on('$stateChangeSuccess', () => {
                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
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
            if (this.$state.params['navbar_right_tab_index'] == 1) {
                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
                return;
            }

            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers))
                .then(response => {
                    var responseData = response.data['data'];

                    // очищаємо попередньо записані маркери які пришли з сервера
                    this.clearResponseMarkers();

                    // якщо з сервера прийшло хоть шось
                    if (angular.isDefined(responseData)) {

                        // якщо обєкт з маркерами який прийшов з сервера має в собі обєкт/обєкти з кольором фільтрів
                        // то цей обєкт містить в собі звичайні маркери (не кругові діаграми)
                        // Тоді видаляємо всі кругові маркери і записуємо звичайні
                        if (angular.isDefined(responseData.blue) || angular.isDefined(responseData.green)) {
                            this.clearPieMarkers();
                            this.responseSimpleMarkers = responseData;
                        }
                        // А інакше видаляємо прості маркери і ставимо кругові
                        else {
                            this.clearSimpleMarkers();
                            this.responsePieMarkers = responseData;
                        }
                    }
                    // інакше видаляємо всі маркери
                    else {
                        this.clearSimpleMarkers();
                        this.clearPieMarkers();
                    }

                    // кажемо всім що маркери загружені
                    this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersIsLoaded'));
                }, response => {
                    // achtung!!1
                });
        }



        public place(map: google.maps.Map) {
            if (this.$state.params['navbar_right_tab_index'] == 1) {
                this.clearSimpleMarkers();
                this.clearPieMarkers();

                console.log(this.favoritesPlaced)
                if (!this.favoritesPlaced)
                    this.placeFavoriteMarkers(map);

                return;
            } else {
                this.clearFavoritesMarkers();
            }

            // якщо обєкт/обєкти з кольором фільтрів з маркерами які прийшли з сервера не пустий
            // то видаляємо лишні і записуємо нові маркери
            if (Object.keys(this.responseSimpleMarkers.blue).length || Object.keys(this.responseSimpleMarkers.green).length) {
                this.intersectionSimpleMarkers(map);

                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
                return;
            }

            // якщо з сервера прийшли не прості а кругові маркери то робимо те саме що і для простих
            if (Object.keys(this.responsePieMarkers).length) {
                this.intersectionPieMarkers(map);

                this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkersPlaced'));
            }
        }



        private placeFavoriteMarkers(map: google.maps.Map) {
            var favoritesMarkers = this.favoritesService.favorites,
                counter = 0;

            console.log(this.favoritesPlaced)

            for (var marker in favoritesMarkers) {
                if (favoritesMarkers.hasOwnProperty(marker)) {
                    var favoriteMarker = favoritesMarkers[marker] || undefined,
                        favoriteMarkerLatLng = `${favoriteMarker.lat}:${favoriteMarker.lng}`;

                    counter += 1;
                    console.log(counter)
                    console.log(favoritesMarkers.length)

                    this.createFavoriteMarker(favoriteMarkerLatLng, map, favoriteMarker);
                }
            }

            if (counter > 0 && counter == favoritesMarkers.length) {
                this.favoritesPlaced = true;
                console.log(this.favoritesMarkers)
            }
        }



        private intersectionSimpleMarkers(map: google.maps.Map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                            var simpleMarker                = this.simpleMarkers[color][latLng]         || undefined,
                                responseSimpleMarker        = this.responseSimpleMarkers[color][latLng] || undefined,
                                responseSimpleMarkerColor   = this.responseSimpleMarkers[color]         || undefined;

                            // Видаляємо маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з одним із кольорів маркерів
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з тілом маркера
                            //  - в обєкті з маркерами який прийшов з сервера ціна маркера відрізняється від ціни існуючого маркера
                            if (angular.isUndefined(responseSimpleMarkerColor)
                                || (angular.isDefined(responseSimpleMarkerColor) && angular.isUndefined(responseSimpleMarker))
                                || simpleMarker.params.price != responseSimpleMarker.price) {

                                this.briefsService.remove(simpleMarker.params.id);

                                console.log('deleted: ' + simpleMarker.params.id);

                                simpleMarker.setMap(null);
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
                            var simpleMarker                = this.simpleMarkers[color][latLng]         || undefined,
                                responseSimpleMarker        = this.responseSimpleMarkers[color][latLng] || undefined;

                            // Додаємо новий маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера є маркер якого нема у вже існуючих маркерах
                            if (angular.isUndefined(simpleMarker)) {
                                this.createSimpleMarker(color, latLng, map, responseSimpleMarker);
                            }
                        }
                    }
                }
            }
        }



        private intersectionPieMarkers(map: google.maps.Map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var latLng in this.pieMarkers) {
                if (this.pieMarkers.hasOwnProperty(latLng)) {
                    var pieMarker           = this.pieMarkers[latLng]           || undefined,
                        responsePieMarker   = this.responsePieMarkers[latLng]   || undefined;

                    // Видаляємо маркер якщо:
                    //  - в обєкті з маркерами який прийшов з сервера немає обєкта з одним із кольорів маркерів
                    //  - в обєкті з маркерами який прийшов з сервера немає обєкта з тілом маркера
                    //  - в обєкті з маркерами який прийшов з сервера ціна маркера відрізняється від ціни існуючого маркера
                    if (angular.isUndefined(responsePieMarker)
                            || pieMarker.params.blue_markers != responsePieMarker.blue
                            || pieMarker.params.green_markers != responsePieMarker.green) {

                        console.log('deleted pie marker: ' + latLng);

                        pieMarker.setMap(null);
                        delete this.pieMarkers[latLng];
                    }
                }
            }

            // додаємо нові маркери на карту
            for (var latLng in this.responsePieMarkers) {
                if (this.responsePieMarkers.hasOwnProperty(latLng)) {
                    var pieMarker                = this.pieMarkers[latLng]         || undefined,
                        responsePieMarker        = this.responsePieMarkers[latLng] || undefined;

                    // Додаємо новий маркер якщо:
                    //  - в обєкті з маркерами який прийшов з сервера є маркер якого нема у вже існуючих маркерах
                    if (angular.isUndefined(pieMarker)) {
                        this.createPieMarker(latLng, map, responsePieMarker);
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

            // якщо маркер є в списку з переглянутими то додаємо йому клас
            if (this._visitedMarkers.indexOf(responseMarker.id) != -1) {
                this.simpleMarkers[color][latLng].labelClass += ' -visited'
            }

            this.simpleMarkers[color][latLng].setMap(map);

            // додаємо бриф для панелі справа
            this.briefsService.add({
                id:             responseMarker.id,
                tid:            responseMarker.tid,
                lat:            markerLat,
                lng:            markerLng,
                price:          responseMarker.price,
                title:          responseMarker.title,
                thumbnail_url:  responseMarker.thumbnail_url
            });

            console.log('added: ' + this.simpleMarkers[color][latLng]);

            this.attachClickEventToSimpleMarker(this.simpleMarkers[color][latLng]);
        }



        private createPieMarker(latLng, map, responseMarker) {
            var markerLat = latLng.split(':')[0],
                markerLng = latLng.split(':')[1],

                // кількість маркерів по кольорах в маркері з діаграмою
                pieBlueMarkers  = responseMarker.blue   || 0,
                pieGreenMarkers = responseMarker.green  || 0,

                // загальна кількість маркерів в маркері з діаграмою
                pieMarkersCount = pieBlueMarkers + pieGreenMarkers,

                // проуентне співвідношення маркерів в маркері з діаграмою
                pieBlueMarkersCountInDeg    = Math.round((360 / 100 * ((pieBlueMarkers / pieMarkersCount) * 100))   || 0),
                pieGreenMarkersCountInDeg   = Math.round((360 / 100 * ((pieGreenMarkers / pieMarkersCount) * 100))  || 0),

                // клас який визначає заливку діаграми в залежності від процентного співвідношення маркерів
                blueAdditionalClass      = pieBlueMarkersCountInDeg  > 180 ? ' full' : '',
                greenAdditionalClass     = pieGreenMarkersCountInDeg > 180 ? ' full' : '',

                // розмір сомого маркера з круговою діаграмою для того що б поміщався весь текст з кількістю
                sizeOfPieChart = pieMarkersCount < 100 ? "small" :
                    pieMarkersCount >= 100 && pieMarkersCount < 1000 ? "medium" :
                        pieMarkersCount >= 1000 && pieMarkersCount < 10000 ? "large" : "super-big",

                // унікальних ключ для класа з діаграмою
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



        private createFavoriteMarker(latLng, map: google.maps.Map, marker) {
            var markerLabelOffsetX = 35,
                markerLat = latLng.split(':')[0],
                markerLng = latLng.split(':')[1];

            if (angular.isDefined(marker.price)) {
                markerLabelOffsetX = this.calcMarkerLabelOffsetX(marker.price.length);
            }

            this.favoritesMarkers[latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    id:     marker.id,
                    tid:    marker.tid,
                    price:  marker.price
                },
                labelContent:
                    `<div class='custom-marker md-whiteframe-z2'>${marker.price}</div>` +
                    `<div class='custom-marker-arrow-down'></div>`,
                labelClass: `custom-marker-container -blue`,
                labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
            });

            this.favoritesMarkers[latLng].setMap(map);

            console.log('added: ' + this.favoritesMarkers[latLng]);

            this.attachClickEventToSimpleMarker(this.favoritesMarkers[latLng]);
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
                                return;
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



        private clearFavoritesMarkers() {
            this.favoritesPlaced = false;

            for (var marker in this.favoritesMarkers) {
                if (this.favoritesMarkers.hasOwnProperty(marker)) {
                    this.favoritesMarkers[marker].setMap(null);
                    delete this.favoritesMarkers[marker];
                }
            }

            this.favoritesMarkers = {};
        }
    }
}