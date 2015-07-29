/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class FiltersService {
        private _filters: Object = {
            map: {
                c: null,                    // city
                l: "48.455935,34.41285",    // lat_lng
                v: null,                    // viewport
                z: 6                        // zoom
            },
            panels: {
                red: {
                    r_t_sid: null
                },
                blue: {
                    b_t_sid: null
                }
            },
            base: {
                // Загальні
                op_sid:     '0',  // operation_sid

                // Дропдауни
                cu_sid:     '0',  // currency_sid
                h_t_sid:    '0',  // heating_type_sid
                pr_sid:     '0',  // period_sid
                pl_sid:     '0',  // planing_sid
                b_t_sid:    '0',  // building_type_sid

                // Поля вводу
                p_min:      null,   // price_min
                p_max:      null,   // price_max
                r_c_min:    null,   // rooms_count_min
                r_c_max:    null,   // rooms_count_max
                f_c_min:    null,   // floors_count_min
                f_c_max:    null,   // floors_count_max
                p_c_min:    null,   // persons_count_min
                p_c_max:    null,   // persons_count_max
                t_a_min:    null,   // total_area_min
                t_a_max:    null,   // total_area_max
                f_min:      null,   // floor_min
                f_max:      null,   // floor_max
                h_a_min:    null,   // halls_area_min
                h_a_max:    null,   // halls_area_max
                c_c_min:    null,   // cabinets_count_min
                c_c_max:    null,   // cabinets_count_max
                h_c_min:    null,   // halls_count_min
                h_c_max:    null,   // halls_count_max
                c_h_min:    null,   // ceiling_height_min
                c_h_max:    null,   // ceiling_height_max
                a_min:      null,   // area_min
                a_max:      null,   // area_max

                // Чекбокси
                n_b:    true,   // new_buildings
                s_m:    true,   // secondary_market
                fml:    false,  // family
                frg:    false,  // foreigners
                elt:    false,  // electricity
                gas:    false,  // gas
                h_w:    false,  // hot_water
                c_w:    false,  // cold_water
                swg:    false,  // sewerage
                lft:    false,  // lift
                sct:    false,  // security
                ktn:    false,  // kitchen
                s_a:    false,  // security_alarm
                f_a:    false,  // fire_alarm
                pit:    false,  // pit
                wtr:    false,  // water
                msd:    true,   // mansard
                grd:    true    // ground
            }
        };
        private _filters_for_load_markers: Object = {
            zoom: null,
            viewport: null,
            filters: []
        };

        public static $inject = [
            '$rootScope',
            '$timeout',
            '$location',
            'TYPES'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $timeout: angular.ITimeoutService,
                    private $location: angular.ILocationService,
                    private TYPES: any) {
            // ---------------------------------------------------------------------------------------------------------

            this.updateFiltersFromUrl();
        }



        public update(filter_object_name: string, filters_object: Object, panel_name?: string) {
            for (var filter in filters_object) {
                if (filters_object.hasOwnProperty(filter)) {
                    if (panel_name) {
                        this._filters[filter_object_name][panel_name][filter] = filters_object[filter];
                    } else {
                        this._filters[filter_object_name][filter] = filters_object[filter];
                    }
                }
            }

            if (panel_name) {
                var panel_prefix = panel_name.toString().substring(0, 1) + "_",
                    type_sid = filter_object_name[panel_prefix + "t_sid"];

                console.log(panel_prefix)
            }

            if (panel_name && type_sid == null) {
                console.log('ddddddddddddddddddd')
                this.createFiltersForPanel(panel_name);
            }

            this.updateUrlFromFilters();
            this.createFormattedObjectForLoadMarkers();

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FiltersService.FiltersUpdated', this._filters));
        }


        public get filters() {
            return this._filters;
        }



        private createFiltersForPanel(panel_color) {
            var self = this,
                panel_prefix        = panel_color.toString().substring(0, 1) + "_",
                type_sid            = this._filters['panels'][panel_color][panel_prefix + 't_sid'],
                location_search     = this.$location.search();


            if (type_sid == null) {
                // Очищаємо обєкт з фільтрами
                this._filters['panels'][panel_color] = {};

                // Створюємо параметр з типом оголошення в обєкті з фільтрами
                //this._filters['panels'][panel_color][panel_prefix + "t_sid"] = type_sid;

                // Видаляємо фільтри з урла
                for (var s_key in location_search) {
                    if (location_search.hasOwnProperty(s_key)) {
                        if (s_key.match(new RegExp('^' + panel_prefix, 'm'))) {
                            this.$location.search(s_key, null);
                        }
                    }
                }
            }


            // Створюємо набір фільтрів для панелі за набором
            if (type_sid != null) {

                var realty_type_filters = self.TYPES.REALTY[type_sid].filters;

                for (var i = 0, len = realty_type_filters.length; i < len; i++) {
                    var filter_name = panel_prefix + realty_type_filters[i];

                    if (angular.isUndefined(this._filters['panels'][panel_color][filter_name])) {
                        this._filters['panels'][panel_color][filter_name] = this._filters['base'][realty_type_filters[i]];
                    }
                }
            }

            console.log(this._filters)

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FiltersService.FiltersUpdated', this._filters));
        }



        private updateFiltersFromUrl() {
            var location_search = this.$location.search(),
                filters_panels = this._filters['panels'];

            for (var key in location_search) {
                if (location_search.hasOwnProperty(key)) {

                    if (key.toString() === "token") {
                        continue;
                    }
                    if (location_search[key] === 'true') {
                        location_search[key] = true;
                    }
                    if (location_search[key] === 'false') {
                        location_search[key] = false;
                    }
                    if (key.toString().indexOf("_sid") !== -1) {
                        location_search[key] = location_search[key];
                    }
                    if (/^r_/.test(key.toString())) {
                        filters_panels['red'][key] = location_search[key];
                    }
                    if (/^b_/.test(key.toString())) {
                        filters_panels['blue'][key] = location_search[key];
                    }
                    if (_.include(['c', 'l', 'z'], key)) {
                        this._filters['map'][key] = location_search[key];
                    }
                }
            }

            if (angular.isUndefined(location_search['r_t_sid']) && angular.isUndefined(location_search['b_t_sid'])) {
                // -
                filters_panels['red']['r_t_sid'] = 0;
                this.createFiltersForPanel("red");
            }
            if (angular.isDefined(location_search['r_t_sid'])) {
                this.createFiltersForPanel("red");
            }
            if (angular.isDefined(location_search['b_t_sid'])) {
                this.createFiltersForPanel("blue");
            }

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FiltersService.UpdatedFromUrl', this._filters));
        }



        private updateUrlFromFilters() {
            var location_search = '',
                map_filters     = this._filters['map'],
                panels_filters  = this._filters['panels'],
                _formattedPanelFilters = {};


            // reset to empty object
            this._filters_for_load_markers = {
                zoom: null,
                viewport: null,
                filters: []
            };


            // create location search from map filters
            for (var map_filter in map_filters) {
                if (map_filters.hasOwnProperty(map_filter) && !_.include(['v'], map_filter)) {
                    if (!map_filters[map_filter]) {
                        continue;
                    }
                    if (!_.include(['', null], map_filters[map_filter])) {
                        location_search += (location_search.length !== 0 ? '&' : '') + map_filter + '=' + map_filters[map_filter];
                    }
                }
            }

            // create location search from panels filters
            for (var panel in panels_filters) {
                if (panels_filters.hasOwnProperty(panel)) {
                    _formattedPanelFilters = {
                        panel: panel
                    };

                    for (var panel_filter in panels_filters[panel]) {
                        if (panels_filters[panel].hasOwnProperty(panel_filter)) {

                            if (panel_filter.indexOf("t_sid") !== -1 && panels_filters[panel][panel_filter] == null) {
                                _formattedPanelFilters = null;
                                continue;
                            }

                            if (_.include(['', null], panels_filters[panel][panel_filter])) {
                                continue;
                            }


                            _formattedPanelFilters[panel_filter.substr(2, panel_filter.length)] = panels_filters[panel][panel_filter];


                            if (panels_filters[panel][panel_filter] === this._filters['base'][panel_filter.substr(2, panel_filter.length)]) {
                                continue;
                            }


                            // i love js
                            //if (_.include(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], filters_panels[panel][filter])) {
                            //    filters_panels[panel][filter] = parseInt(filters_panels[panel][filter]);
                            //}

                            location_search += (location_search.length !== 0 ? '&' : '') + panel_filter + '=' + panels_filters[panel][panel_filter];
                        }
                    }

                    if (_formattedPanelFilters != null)
                        this._filters_for_load_markers['filters'].push(_formattedPanelFilters);


                }
            }

            console.info('updateUrlFromPanelsFilters method: panels filters updated');

            this.$location.search(location_search);

            if (!this.$rootScope.$$phase)
                this.$rootScope.$apply();
        }



        private createFormattedObjectForLoadMarkers() {
            this._filters_for_load_markers['zoom'] = this._filters['map']['z'];
            this.createFormattedViewportForLoadMarkers();

            this.$timeout(() => this.$rootScope.$broadcast('Mappino.Map.FiltersService.CreatedFormattedFilters', this._filters_for_load_markers));
        }



        private createFormattedViewportForLoadMarkers() {
            var filters_map = this._filters['map'];

            var sneLat = filters_map['v'].getNorthEast().lat().toString(),
                sneLng = filters_map['v'].getNorthEast().lng().toString(),
                sswLat = filters_map['v'].getSouthWest().lat().toString(),
                sswLng = filters_map['v'].getSouthWest().lng().toString();

            var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
                neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
                swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
                swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), "");

            this._filters_for_load_markers['viewport'] = {
                'ne_lat': neLat,
                'ne_lng': neLng,
                'sw_lat': swLat,
                'sw_lng': swLng
            };

            console.log(this._filters_for_load_markers)
        }
    }
}