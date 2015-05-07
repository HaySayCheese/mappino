


module pages.map {
    'use strict';

    export class FiltersService {
        private _filters: Object = {
            map: {
                c: null,    // city
                l: "48.455935,34.41285",    // lat_lng
                v: null,    // viewport
                z: 6     // zoom
            },
            panels: {
                red: {
                    r_t_sid: null
                },
                blue: {
                    b_t_sid: null
                },
                green: {
                    g_t_sid: null
                },
                yellow: {
                    y_t_sid: null
                }
            },
            base: {
                // Загальні
                op_sid:     0,  // operation_sid

                // Дропдауни
                cu_sid:     0,  // currency_sid
                h_t_sid:    0,  // heating_type_sid
                pr_sid:     0,  // period_sid
                pl_sid:     0,  // planing_sid
                b_t_sid:    0,  // building_type_sid

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

        public static $inject = [
            '$rootScope',
            '$timeout',
            '$location',
            'RealtyTypesService'
        ];

        constructor(private $rootScope: angular.IRootScopeService,
                    private $timeout: angular.ITimeoutService,
                    private $location: angular.ILocationService,
                    private realtyTypesService: bModules.Types.RealtyTypesService) {
            // -
            this.updateFiltersFromUrl();
            this.updateUrlFromPanelsFilters();
        }



        public update(filter_object: string, filter_name: string, filter_value: any) {
            this._filters[filter_object][filter_name] = filter_value;

            if (filter_object === 'map') {
                this.updateUrlFromMapFilters();
            } else {
                this.updateUrlFromPanelsFilters();
            }

            console.log(this._filters)
        }


        get filters() {
            return this._filters;
        }



        private createFiltersForPanel(panel_color, clear_previously) {
            var self = this,
                panel_prefix        = panel_color.toString().substring(0, 1) + "_",
                type_sid            = this._filters['panels'][panel_color][panel_prefix + 't_sid'],
                location_search     = this.$location.search();


            if (clear_previously) {
                // Очищаємо обєкт з фільтрами
                this._filters['panels'][panel_color] = {};

                // Створюємо параметр з типом оголошення в обєкті з фільтрами
                this._filters['panels'][panel_color][panel_prefix + "t_sid"] = type_sid;

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
            if (!_.isNull(type_sid)) {
                var realty_type_filters = _.where(self.realtyTypesService.realty_types, { 'id': type_sid })[0]['filters'];

                for (var i = 0, len = realty_type_filters.length; i < len; i++) {
                    var filter_name = panel_prefix + realty_type_filters[i];

                    if (_.isUndefined(this._filters['panels'][panel_color][filter_name])) {
                        this._filters['panels'][panel_color][filter_name] = this._filters['base'][realty_type_filters[i]];
                    }
                }
            }
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
                        location_search[key] = parseInt(location_search[key]);
                    }
                    if (/^r_/.test(key.toString())) {
                        filters_panels['red'][key] = location_search[key];
                    }
                    if (/^b_/.test(key.toString())) {
                        filters_panels['blue'][key] = location_search[key];
                    }
                    if (/^g_/.test(key.toString())) {
                        filters_panels['green'][key] = location_search[key];
                    }
                    if (/^y_/.test(key.toString())) {
                        filters_panels['yellow'][key] = location_search[key];
                    }
                    if (_.include(['c', 'l', 'z'], key)) {
                        this._filters['map'][key] = location_search[key];
                    }
                }
            }

            if (_.isUndefined(location_search['r_t_sid']) && _.isUndefined(location_search['b_t_sid']) &&
                _.isUndefined(location_search['g_t_sid']) && _.isUndefined(location_search['y_t_sid'])) {
                // -
                filters_panels['red']['r_t_sid'] = 0;
                this.createFiltersForPanel("red", false);
            }
            if (!_.isUndefined(location_search['r_t_sid'])) {
                this.createFiltersForPanel("red", false);
            }
            if (!_.isUndefined(location_search['b_t_sid'])) {
                this.createFiltersForPanel("blue", false);
            }
            if (!_.isUndefined(location_search['g_t_sid'])) {
                this.createFiltersForPanel("green", false);
            }
            if (!_.isUndefined(location_search['y_t_sid'])) {
                this.createFiltersForPanel("yellow", false);
            }

            this.$timeout(() => this.$rootScope.$broadcast('pages.map.FiltersService.UpdatedFromUrl', this._filters));

            console.log(this._filters)
        }



        private updateUrlFromMapFilters() {
            var filters_map = this._filters['map'];

            for (var filter in filters_map) {
                if (filters_map.hasOwnProperty(filter) && !_.include(['v'], filter)) {
                    console.log('update map filters in url')
                    this.$location.search(filter, filters_map[filter]);

                    if (!this.$rootScope.$$phase)
                        this.$rootScope.$apply();
                }
            }
        }



        private updateUrlFromPanelsFilters() {
            var location_search = '',
                filters_panels = this._filters['panels'];

            for (var panel in filters_panels) {
                if (filters_panels.hasOwnProperty(panel)) {
                    for (var filter in filters_panels[panel]) {
                        if (filters_panels[panel].hasOwnProperty(filter)) {

                            if (filter.indexOf("t_sid") !== -1 && _.isNull(filters_panels[panel][filter])) {
                                continue;
                            }

                            // i love js
                            if (_.include(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], filters_panels[panel][filter])) {
                                filters_panels[panel][filter] = parseInt(filters_panels[panel][filter]);
                            }

                            // _.include(['true', true, 'false', false], panel_filters[filter])
                            // - примусово записуємо булеве значення в урл (по дефолту ангулар не пише буль в урл)
                            //
                            // panel_filters[filter] !== filters.base[filter.substr(2, filter.length)]
                            // - провіряємо чи значення фільтра в урлі !== значенню фільтра в базовому наборі
                            // таким чином скорочуємо сам урл не засоряючи його фільтрами які вже є в памяті
                            // геніально :)
                            if (_.include(['true', true, 'false', false], filters_panels[panel][filter]) &&
                                filters_panels[panel][filter] !== this._filters['base'][filter.substr(2, filter.length)]) {
                                // -
                                location_search += (location_search.length !== 0 ? '&' : '') + filter + '=' + filters_panels[panel][filter];
                                continue;
                            }

                            // якщо фільтер пустий і цей фільтр є zoom/latLng/viewport то не пишемо його в параметри
                            // тому що ці фільтри треба писати в $routeParams а не $location.search()
                            // а якщо не пустий і відрізняється від стандарного то пишем в $location.search()
                            if (_.include(['', null], filters_panels[panel][filter])) {
                                // todo: причесати
                            } else if (filters_panels[panel][filter] !== this._filters['base'][filter.substr(2, filter.length)]) {
                                location_search += (location_search.length !== 0 ? '&' : '') + filter + '=' + filters_panels[panel][filter];
                            }
                        }
                    }
                }
            }

            console.log('update panels filters in url')
            console.log(location_search)

            this.$location.search(location_search);

            if (!this.$rootScope.$$phase)
                this.$rootScope.$apply();
            //$rootScope.searchUrlPart = base64.urlencode(location_search);
            //$location.search(base64.urlencode(location_search));
        }
    }
}