/**
 * Filters factory
 *
 * todo: write description here
 **/
app.factory('FiltersFactory', ['$location', 'PublicationTypesFactory', function($location, PublicationTypesFactory) {
    "use strict";

    var filters = {
        map: {
            c: "",                      // city
            z: parseInt(6),             // zoom
            l: "48.455935, 34.41285",   // latLng
            v: null                     // viewport
        },

        base: {
            // Загальні
            op_sid: 0,   // operation_sid

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
        },

        red: {
            r_t_sid: 0
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
    };
    var _tempViewportFromHomePage;

    return {
        /**
         * @description Create filters collection for panel from 'PublicationTypes.filters'
         *
         * @example
         * FiltersFactory.createFiltersForPanel('red', true/false);
         *
         * @param {String} panelColor               - Color of sidebar filters panel
         * @param {Boolean} clearPreviousFilters    - Remove filters object when true
         **/
        createFiltersForPanel: function(panelColor, clearPreviousFilters) {
            var panelColorPrefix        = panelColor.toString().substring(0, 1) + "_",
                type_sid                = filters[panelColor][panelColorPrefix + 't_sid'],
                searchParameters        = $location.search();


            if (clearPreviousFilters) {
                // Очищаємо обєкт з фільтрами
                filters[panelColor] = {};

                // Створюємо параметр з типом оголошення в обєкті з фільтрами
                filters[panelColor][panelColorPrefix + "t_sid"] = type_sid;

                // Видаляємо фільтри з урла
                for (var s_key in searchParameters) {
                    if (searchParameters.hasOwnProperty(s_key)) {
                        if (s_key.match(new RegExp('^' + panelColorPrefix, 'm'))) {
                            $location.search(s_key, null);
                        }
                    }
                }
            }


            // Створюємо набір фільтрів для панелі за набором з 'PublicationTypes'
            if (!_.isNull(type_sid)) {
                var availableTypeFilters = PublicationTypesFactory.getAvailableTypeFiltersById(type_sid);

                for (var i = 0; i < availableTypeFilters.length; i++) {
                    var filterName = panelColorPrefix + availableTypeFilters[i];

                    if (!filters[panelColor][filterName]) {
                        filters[panelColor][filterName] = filters.base[availableTypeFilters[i]];
                    }
                }
            }
        },


        /**
         * @description Update filters from url search parameters
         *
         * @example
         * FiltersFactory.updateFiltersFromUrl();
         **/
        updateFiltersFromUrl: function() {
            var searchParameters = $location.search();

            for (var key in searchParameters) {
                if (searchParameters.hasOwnProperty(key)) {

                    if (key.toString() === "token") {
                        continue;
                    }

                    if (key.toString().indexOf("_sid") !== -1) {
                        searchParameters[key] = parseInt(searchParameters[key]);
                    }

                    if (/^r_/.test(key.toString())) {
                        filters.red[key] = searchParameters[key];
                    }

                    if (/^b_/.test(key.toString())) {
                        filters.blue[key] = searchParameters[key];
                    }

                    if (/^g_/.test(key.toString())) {
                        filters.green[key] = searchParameters[key];
                    }

                    if (/^y_/.test(key.toString())) {
                        filters.yellow[key] = searchParameters[key];
                    }

                    if (_.include(['c', 'z', 'l'], key)) {
                        filters.map[key] = searchParameters[key];
                    }
                }
            }

            searchParameters['r_t_sid'] ? this.createFiltersForPanel("red", false) :
                searchParameters['b_t_sid'] ? this.createFiltersForPanel("blue", false) :
                    searchParameters['g_t_sid'] ? this.createFiltersForPanel("green", false) :
                        searchParameters['y_t_sid'] ? this.createFiltersForPanel("yellow", false) : this.createFiltersForPanel("red", false);
        },



        /**
         * @description Update url search parameters from filters
         *
         * @example
         * FiltersFactory.updateUrlFromFilters($scope.filters.red);
         *
         * @param {Object} filters - Filters object
         **/
        updateUrlFromFilters: function(filters) {
            for (var filter in filters) {
                if (filters.hasOwnProperty(filter)) {

                    if (filter.indexOf("t_sid") !== -1 && _.isNull(filters[filter])) {
                        return false;
                    }

                    if (_.include(["0", 0], filters[filter])) {
                        $location.search(filter, filters[filter]);
                        continue;
                    }

                    if (_.include(['', null, false, 'false'], filters[filter]) || filter === "v") {
                        $location.search(filter, null);
                    } else {
                        $location.search(filter, filters[filter]);
                    }
                }
            }
        },


        getFilters: function() {
            return filters;
        },

        getSidebarTemplateUrl: function() {
            // todo: написати логіку для віддачі урла для ріелторів
            return "/ajax/template/main/sidebar/common/";
        }
    };
}]);