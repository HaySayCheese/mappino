
namespace Mappino.Map {
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

        private requests = {
            load: []
        };

        public static $inject = [
            '$rootScope',
            '$state',
            '$http',
            '$timeout',
            '$q',
            'PublicationHandler',
            'BriefsService',
            'FavoritesService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $state: angular.ui.IStateService,
                    private $http: angular.IHttpService,
                    private $timeout: angular.ITimeoutService,
                    private $q: angular.IQService,
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
            $rootScope.$on('Mappino.Map.BriefsService.BriefMouseLeave', event => this.clearHighlight('hover'));
            $rootScope.$on('Mappino.Map.PublicationService.PublicationActive', (event, markerId) => this.highlightMarker(markerId, 'active'));
            $rootScope.$on('Mappino.Map.PublicationService.PublicationClosed', event => this.clearHighlight('active'));
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

            this.cancelRequestsByGroup('load');

            var deffer = this.$q.defer();
            this.requests.load.push(deffer);

            this.$http.get('/ajax/api/markers/?p=' + angular.toJson(this._filters_for_load_markers), {
                timeout: deffer.promise
            }).then(response => {
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
            } else if (!Object.keys(this.responseSimpleMarkers.blue).length) {
                this.clearSimpleMarkers('blue');
            } else if (!Object.keys(this.responseSimpleMarkers.green).length) {
                this.clearSimpleMarkers('green');
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

            for (var marker in favoritesMarkers) {
                if (favoritesMarkers.hasOwnProperty(marker)) {
                    var favoriteMarker = favoritesMarkers[marker] || undefined,
                        favoriteMarkerLatLng = `${favoriteMarker.lat}:${favoriteMarker.lng}`;

                    counter += 1;

                    this.createFavoriteMarker(favoriteMarkerLatLng, map, favoriteMarker);
                }
            }

            if (counter > 0 && counter == favoritesMarkers.length) {
                this.favoritesPlaced = true;
            }
        }



        private intersectionSimpleMarkers(map: google.maps.Map) {
            // видаляємо маркери з карти яких нема в відповіді з сервера
            for (var color in this.simpleMarkers) {
                if (this.simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in this.simpleMarkers[color]) {
                        if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                            var simpleMarker = this.simpleMarkers[color][latLng];

                            //console.log(responseSimpleMarker)
                            // Видаляємо маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з одним із кольорів маркерів
                            //  - в обєкті з маркерами який прийшов з сервера немає обєкта з тілом маркера
                            //  - в обєкті з маркерами який прийшов з сервера ціна маркера відрізняється від ціни існуючого маркера
                            if (angular.isUndefined(this.responseSimpleMarkers[color])
                                || (angular.isDefined(this.responseSimpleMarkers[color]) && angular.isUndefined(this.responseSimpleMarkers[color][latLng]))
                                || simpleMarker.params.price != this.responseSimpleMarkers[color][latLng].price) {

                                this.briefsService.remove(simpleMarker.params.hid);

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
                            var responseSimpleMarker = this.responseSimpleMarkers[color][latLng];

                            // Додаємо новий маркер якщо:
                            //  - в обєкті з маркерами який прийшов з сервера є маркер якого нема у вже існуючих маркерах
                            if (angular.isUndefined(this.simpleMarkers[color][latLng])) {
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

            //noinspection TypeScriptUnresolvedFunction
            this.simpleMarkers[color][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    hid:    responseMarker.hid,
                    tid:    responseMarker.tid,
                    d0:     responseMarker.d0,
                    price:  responseMarker.price
                },
                labelContent:
                    `<div class='custom-marker md-whiteframe-z2'>${responseMarker.price}, ${responseMarker.d0}к</div>` +
                    `<div class='custom-marker-arrow-down'></div>`,
                labelClass: `custom-marker-container -${color}`,
                labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
            });

            // якщо маркер є в списку з переглянутими то додаємо йому клас
            if (this._visitedMarkers.indexOf(responseMarker.hid) != -1) {
                this.simpleMarkers[color][latLng].labelClass += ' -visited'
            }

            // якщо в урлі є ід цього маркера то додаємо йому клас з підсвіткою
            if (this.$state.params['publication_id'].split(':')[1] == responseMarker.hid) {
                if (this.simpleMarkers[color][latLng].labelClass.indexOf('-active') == -1)
                    this.simpleMarkers[color][latLng].labelClass += ' -active'
            }

            this.simpleMarkers[color][latLng].setMap(map);

            // додаємо бриф для панелі справа
            this.briefsService.add({
                tid:            responseMarker.tid,
                hid:            responseMarker.hid,
                lat:            markerLat,
                lng:            markerLng,
                d0:             responseMarker.d0,
                price:          responseMarker.price,
                title:          responseMarker.title,
                thumbnail_url:  responseMarker.thumbnail_url,
                is_favorite:    false
            });

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
                blueAdditionalClass      = pieBlueMarkersCountInDeg  > 180 ? 'full' : '',
                greenAdditionalClass     = pieGreenMarkersCountInDeg > 180 ? 'full' : '',

                // розмір сомого маркера з круговою діаграмою для того що б поміщався весь текст з кількістю
                sizeOfPieChart = pieMarkersCount < 100 ? "small" :
                    pieMarkersCount >= 100 && pieMarkersCount < 1000 ? "medium" :
                        pieMarkersCount >= 1000 && pieMarkersCount < 10000 ? "large" : "super-big",

                // унікальних ключ для класа з діаграмою
                _uuid = _.uniqueId('pie-marker-');


            //noinspection TypeScriptUnresolvedFunction
            this.pieMarkers[latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    count:              pieMarkersCount,
                    blue_markers:       pieBlueMarkers,
                    green_markers:      pieGreenMarkers
                },
                labelContent:
                    `<style>
                        .${_uuid}.pie.pie-blue {
                            transform: rotate(0deg);
                        }
                        .${_uuid}.pie.pie-blue:before {
                            transform: rotate(${pieBlueMarkersCountInDeg}deg);
                        }
                        .${_uuid}.pie.pie-green {
                            transform: rotate(${pieBlueMarkersCountInDeg}deg);
                        }
                        .${_uuid}.pie.pie-green:before {
                            transform: rotate(${pieGreenMarkersCountInDeg}deg);
                        }
                    </style>
                    <div>
                        <div class='marker-pie-chart-inner'>${pieMarkersCount}</div>
                        <div class='${_uuid} pie pie-blue ${blueAdditionalClass}'></div>
                        <div class='${_uuid} pie pie-green ${greenAdditionalClass}'></div>
                    </div>`,
                labelClass: `marker-pie-chart ${sizeOfPieChart} md-whiteframe-z2`,
                labelAnchor: new google.maps.Point(30, 45),
            });

            this.pieMarkers[latLng].setMap(map);

            this.attachClickEventToPieMarker(this.pieMarkers[latLng], map);
        }



        private createFavoriteMarker(latLng, map: google.maps.Map, marker) {
            var markerLabelOffsetX = 35,
                markerLat = latLng.split(':')[0],
                markerLng = latLng.split(':')[1];

            if (angular.isDefined(marker.price)) {
                markerLabelOffsetX = this.calcMarkerLabelOffsetX(marker.price.length);
            }

            //noinspection TypeScriptUnresolvedFunction
            this.favoritesMarkers[latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(markerLat, markerLng),
                icon: '/../mappino_static/build/images/markers/empty_marker.png',
                params: {
                    hid:    marker.hid,
                    tid:    marker.tid,
                    d0:     marker.d0,
                    price:  marker.price
                },
                labelContent:
                    `<div class='custom-marker md-whiteframe-z2'>${marker.price}, ${marker.d0}к</div>` +
                    `<div class='custom-marker-arrow-down'></div>`,
                labelClass: `custom-marker-container -pink`,
                labelAnchor: new google.maps.Point(markerLabelOffsetX, 37)
            });

            // якщо в урлі є ід цього маркера то додаємо йому клас з підсвіткою
            if (this.$state.params['publication_id'].split(':')[1] == marker.hid) {
                if (this.favoritesMarkers[latLng].labelClass.indexOf('-active') == -1)
                    this.favoritesMarkers[latLng].labelClass += ' -active'
            }

            this.favoritesMarkers[latLng].setMap(map);

            this.attachClickEventToSimpleMarker(this.favoritesMarkers[latLng]);
        }



        private attachClickEventToPieMarker(marker, map) {
            google.maps.event.addListener(marker, 'click', () => {
                map.panTo(marker.getPosition());
                map.setZoom(map.getZoom() + 1);
            });
        }



        private attachClickEventToSimpleMarker(marker) {
            google.maps.event.addListener(marker, 'click', () => {
                this.publicationHandler.open(`${marker.params.tid}:${marker.params.hid}`);
            });

            google.maps.event.addListener(marker, 'mouseover', () => {
                this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkerMouseOver', marker.params.hid);
            });

            google.maps.event.addListener(marker, 'mouseout', () => {
                this.$rootScope.$broadcast('Mappino.Map.MarkersService.MarkerMouseOut', marker.params.hid);
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
            var ACTION_CLASS    = null,
                ACTIVE_CLASS    = '-active';

            switch (action) {
                case 'hover':
                    ACTION_CLASS = '-hover';
                    break;
                case 'active':
                    ACTION_CLASS = '-active';
                    break;
                case 'visited':
                    ACTION_CLASS = '-visited';
                    break;
            }

            var simpleMarkers       = this.simpleMarkers,
                favoritesMarkers    = this.favoritesMarkers;

            for (var color in simpleMarkers) {
                if (simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in simpleMarkers[color]) {
                        if (simpleMarkers[color].hasOwnProperty(latLng)) {
                            var marker = simpleMarkers[color][latLng];
                            var markerMap = marker.getMap();

                            if (marker.params.hid == markerId && marker.labelClass.indexOf(ACTION_CLASS) == -1) {
                                if (marker.labelClass.indexOf(ACTIVE_CLASS) == -1) {
                                    marker.labelClass += ` ${ACTION_CLASS}`;
                                    marker.setMap(null);
                                    marker.setMap(markerMap);
                                }
                            }
                        }
                    }
                }
            }

            for (var marker in favoritesMarkers) {
                if (favoritesMarkers.hasOwnProperty(marker)) {
                    var marker = favoritesMarkers[marker];
                    var markerMap = marker.getMap();

                    if (marker.params.hid == markerId && marker.labelClass.indexOf(ACTION_CLASS) == -1) {
                        if (marker.labelClass.indexOf(ACTIVE_CLASS) == -1) {
                            marker.labelClass += ` ${ACTION_CLASS}`;
                            marker.setMap(null);
                            marker.setMap(markerMap);
                        }
                    }
                }
            }
        }



        private clearHighlight(action) {
            var ACTION_CLASS = null;

            switch (action) {
                case 'hover':
                    ACTION_CLASS = '-hover';
                    break;
                case 'active':
                    ACTION_CLASS = '-active';
                    break;
            }

            var simpleMarkers       = this.simpleMarkers,
                favoritesMarkers    = this.favoritesMarkers;

            for (var color in simpleMarkers) {
                if (simpleMarkers.hasOwnProperty(color)) {
                    for (var latLng in simpleMarkers[color]) {
                        if (simpleMarkers[color].hasOwnProperty(latLng)) {
                            var marker      = simpleMarkers[color][latLng],
                                markerMap   = marker.getMap();

                            if (marker.labelClass.indexOf(ACTION_CLASS) != -1) {
                                marker.labelClass = marker.labelClass.substring(0, marker.labelClass.indexOf(ACTION_CLASS));
                                marker.setMap(null);
                                marker.setMap(markerMap)
                            }
                        }
                    }
                }
            }


            for (var marker in favoritesMarkers) {
                if (favoritesMarkers.hasOwnProperty(marker)) {
                    var marker      = favoritesMarkers[marker],
                        markerMap   = marker.getMap();

                    if (marker.labelClass.indexOf(ACTION_CLASS) != -1) {
                        marker.labelClass = marker.labelClass.substring(0, marker.labelClass.indexOf(ACTION_CLASS));
                        marker.setMap(null);
                        marker.setMap(markerMap)
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



        private clearSimpleMarkers(color?: any) {
            if (color) {
                var simpleMarkers = this.simpleMarkers;

                for (var latLng in simpleMarkers[color]) {
                    if (simpleMarkers[color].hasOwnProperty(latLng)) {
                        this.briefsService.remove(simpleMarkers[color][latLng].params.hid);
                        simpleMarkers[color][latLng].setMap(null);
                        delete simpleMarkers[color][latLng];
                    }
                }
                this.simpleMarkers[color] = {};
            } else {
                for (var color in this.simpleMarkers) {
                    if (this.simpleMarkers.hasOwnProperty(color)) {
                        for (var latLng in this.simpleMarkers[color]) {
                            if (this.simpleMarkers[color].hasOwnProperty(latLng)) {
                                this.briefsService.remove(this.simpleMarkers[color][latLng].params.hid);
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



        private cancelRequestsByGroup(groupName: string) {
            var requests = this.requests[groupName] || {};

            if (!requests) return;

            for (var request in requests) {
                if (requests.hasOwnProperty(request)) {
                    this.requests[groupName][request].resolve();
                }
            }
        }
    }
}