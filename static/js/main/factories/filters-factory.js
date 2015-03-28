/**
 * Filters factory
 *
 * todo: write description here
 **/
app.factory('FiltersFactory', ['$location', '$route', 'base64', 'PublicationTypesFactory',
    function($location, $route, base64, PublicationTypesFactory) {
        "use strict";

        var filters = {
            map: {
                c: "",                      // city
                z: parseInt(6),             // zoom
                l: "48.455935,34.41285",    // latLng
                v: null                     // viewport
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
            },

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
        };

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

                        if (_.isUndefined(filters[panelColor][filterName])) {
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
                var searchParameters = '';

                /* Дешифруємо фільтри з урла */
                if (_.keys($location.search()).length !== 0) {
                    var encodedString   = base64.urldecode(_.keys($location.search())[0]),
                        formattedString = encodedString.replace(/&/g, ",").replace(/=/g, ":"),
                        formattedArray  = formattedString.split(',');
                    var keys = [],
                        values = [];

                    for (var i = 0; i < formattedArray.length; i++) {
                        keys.push(formattedArray[i].split(':')[0]);
                        values.push(formattedArray[i].split(':')[1]);
                    }

                    searchParameters = _.object(keys, values);
                }
                /* кінець дешифратора :) */


                for (var key in searchParameters) {
                    if (searchParameters.hasOwnProperty(key)) {

                        if (key.toString() === "token") {
                            continue;
                        }
                        if (searchParameters[key] === 'true') {
                            searchParameters[key] = true;
                        }
                        if (searchParameters[key] === 'false') {
                            searchParameters[key] = false;
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

                        if (_.include(['c'], key)) {
                            filters.map[key] = searchParameters[key];
                        }
                    }
                }

                if (_.isUndefined(searchParameters['r_t_sid']) && _.isUndefined(searchParameters['b_t_sid'])
                    && _.isUndefined(searchParameters['g_t_sid']) && _.isUndefined(searchParameters['y_t_sid'])) {

                    filters.red.r_t_sid = 0;
                    this.createFiltersForPanel("red", false);
                }
                if (!_.isUndefined(searchParameters['r_t_sid'])) {
                    this.createFiltersForPanel("red", false);
                }
                if (!_.isUndefined(searchParameters['b_t_sid'])) {
                    this.createFiltersForPanel("blue", false);
                }
                if (!_.isUndefined(searchParameters['g_t_sid'])) {
                    this.createFiltersForPanel("green", false);
                }
                if (!_.isUndefined(searchParameters['y_t_sid'])) {
                    this.createFiltersForPanel("yellow", false);
                }
            },



            /**
             * @description Update url search parameters from filters
             *
             * @example
             * FiltersFactory.updateUrlFromFilters($scope.filters.red);
             **/
            updateUrlFromFilters: function() {
                var searchParameters = '';

                for (var filtersObject in filters) {
                    if (filtersObject === 'base') {
                        continue;
                    }

                    for (var filter in filters[filtersObject]) {
                        if (filters[filtersObject].hasOwnProperty(filter)) {

                            if (filter.indexOf("t_sid") !== -1 && _.isNull(filters[filtersObject][filter])) {
                                continue;
                            }


                            // i love js
                            if (_.include(["0", '1', '2', '3', '4', '5', '6', '7', '8', '9'], filters[filtersObject][filter])) {
                                filters[filtersObject][filter] = parseInt(filters[filtersObject][filter]);
                            }

                            //if (searchParameters.length !== 1) {
                            //    searchParameters += '&';
                            //}
                            // _.include(['true', true, 'false', false], panel_filters[filter])
                            // - примусово записуємо булеве значення в урл (по дефолту ангулар не пише буль в урл)
                            //
                            // panel_filters[filter] !== filters.base[filter.substr(2, filter.length)]
                            // - провіряємо чи значення фільтра в урлі !== значенню фільтра в базовому наборі
                            // таким чином скорочуємо сам урл не засоряючи його фільтрами які вже є в памяті
                            // геніально :)
                            if (_.include(['true', true, 'false', false], filters[filtersObject][filter]) && filters[filtersObject][filter] !== filters.base[filter.substr(2, filter.length)]) {
                                searchParameters += (searchParameters.length !== 0 ? '&' : '') + filter + '=' + filters[filtersObject][filter];
                                continue;
                            }

                            // якщо фільтер пустий і цей фільтр є zoom/latLng/viewport то не пишемо його в параметри
                            // тому що ці фільтри треба писати в $routeParams а не $location.search()
                            // а якщо не пустий і відрізняється від стандарного то пишем в $location.search()
                            if (_.include(['', null], filters[filtersObject][filter]) || _.include(['z', 'l', 'v'], filter)) {
                                // todo: причесати
                            } else if (filters[filtersObject][filter] !== filters.base[filter.substr(2, filter.length)]) {
                                searchParameters += (searchParameters.length !== 0 ? '&' : '') + filter + '=' + filters[filtersObject][filter];
                            }
                        }
                    }
                }

                //$location.search(searchParameters);
                $location.search(base64.urlencode(searchParameters));
            },



            /**
             * @description Update url map parameters (latLng and zoom)
             *
             * @example
             * FiltersFactory.updateMapParametersInUrl();
             **/
            updateMapParametersInUrl: function() {
                $route.updateParams({
                    zoom:   filters.map.z,
                    latLng: filters.map.l
                });
            },



            /**
             * @description Return a formatted viewport for Dima )
             *
             * @example
             * FiltersFactory.getFormattedViewport();
             *
             * @returns {Object} - Formatted viewport
             **/
            getFormattedViewport: function() {
                var sneLat = filters.map.v.getNorthEast().lat().toString(),
                    sneLng = filters.map.v.getNorthEast().lng().toString(),
                    sswLat = filters.map.v.getSouthWest().lat().toString(),
                    sswLng = filters.map.v.getSouthWest().lng().toString();

                var neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), ""),
                    neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), ""),
                    swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), ""),
                    swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), "");

                return {
                    'ne_lat': neLat,
                    'ne_lng': neLng,
                    'sw_lat': swLat,
                    'sw_lng': swLng
                };
            },



            /**
             * @description Return all filters object
             *
             * @example
             * FiltersFactory.getFilters();
             *
             * @returns {Object} - Filters object
             **/
            getFilters: function() {
                return filters;
            },



            /**
             * @description Return sidebar template url
             *
             * @example
             * FiltersFactory.getSidebarTemplateUrl();
             *
             * @returns {String} - Sidebar template url
             **/
            getSidebarTemplateUrl: function() {
                // todo: написати логіку для віддачі урла для ріелторів
                return "/ajax/template/main/sidebar/common/";
            }
        };
    }
]);