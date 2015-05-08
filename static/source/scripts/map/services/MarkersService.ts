/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MarkersService {
        private _filters_for_load_markers: any;
        private _load_markers_canceler: any;

        private _response_markers: any = {
            red: {
                '47.8125:25.87522': 1
            }
        };
        private _markers_to_remove: any = {
            red: {}
        };
        private _markers_to_place: any = {
            red: {}
        };

        public static $inject = [
            '$rootScope',
            '$http',
            '$q',
            '$timeout'
        ];

        constructor(
            private $rootScope: angular.IRootScopeService,
            private $http: angular.IHttpService,
            private $q: angular.IQService,
            private $timeout: angular.ITimeoutService) {
            // -
            var self = this;

            $rootScope.$on('pages.map.FiltersService.CreatedFormattedFilters', function(event, formatted_filters) {
                self._filters_for_load_markers = formatted_filters;
                console.log(JSON.stringify(self._filters_for_load_markers))

                self.load();
            });
        }



        private load() {
            var self = this;

            if (this._load_markers_canceler)
                this._load_markers_canceler.resolve();

            this._load_markers_canceler = this.$q.defer();

            this.$http.get('/ajax/api/markers/?p=' + JSON.stringify(this._filters_for_load_markers), {
                timeout: this._load_markers_canceler.promise
            }).success(function(response) {
                self._response_markers = response;
                self.intersection(response);
            });
        }



        private intersection(_new_response_markers: any) {
            var self = this;

            self._markers_to_place['red'] = {};
            self._response_markers['red']['47.8125111:25.87522'] = 1;

            console.log(self._response_markers)
            console.log(_new_response_markers)


            // find unique
            for (var panel in _new_response_markers) {
                if (_new_response_markers.hasOwnProperty(panel)) {
                    for (var marker in _new_response_markers[panel]) {
                        if (_new_response_markers[panel].hasOwnProperty(marker)) {
                            if (_.isUndefined(self._response_markers[panel][marker])) {
                                self._markers_to_place[panel][marker] = _new_response_markers[panel][marker];
                                //self._response_markers[panel][marker] = _new_response_markers[panel][marker];
                                console.log(self._markers_to_place)
                            }
                        }
                    }
                }
            }


            // find old
            for (var panel in self._response_markers) {
                if (self._response_markers.hasOwnProperty(panel)) {
                    for (var marker in self._response_markers[panel]) {
                        if (self._response_markers[panel].hasOwnProperty(marker)) {
                            if (_.isUndefined(_new_response_markers[panel][marker])) {
                                self._markers_to_remove[panel][marker] = self._response_markers[panel][marker];
                                console.log(self._markers_to_remove)
                            }
                        }
                    }
                }
            }

            this.$timeout(() => this.$rootScope.$broadcast('pages.map.MarkersService.MarkersDone'));
        }



        public place(map) {
            for (var panel in this._markers_to_place) {
                if (this._markers_to_place.hasOwnProperty(panel)) {
                    for (var marker in this._markers_to_place[panel]) {
                        if (this._markers_to_place[panel].hasOwnProperty(marker)) {
                            var _marker = new google.maps.Marker({
                                position: new google.maps.LatLng(marker.split(':')[0], marker.split(':')[1]),
                                map: map,
                                title: 'Hello World!'
                            });
                            console.log('place')
                        }
                    }
                }
            }
        }
    }
}