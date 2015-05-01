'use strict'

###*
    # @class
    # @description todo: add desc
    # @version 0.0.1
    # @license todo: add license
    ###
class MFiltersService
    constructor: (@http, @location, @base64) ->
        @filters =
            map:
                c: null                     # city
                z: parseInt(6)              # zoom
                l: "48.455935,34.41285"     # latLng
                v: null                     # viewport
            base:
                # drop downs
                op_sid:     0  # operation_sid
                cu_sid:     0  # currency_sid
                h_t_sid:    0  # heating_type_sid
                pr_sid:     0  # period_sid
                pl_sid:     0  # planing_sid
                b_t_sid:    0  # building_type_sid

                # fields
                p_min:      null   # price_min
                p_max:      null   # price_max
                r_c_min:    null   # rooms_count_min
                r_c_max:    null   # rooms_count_max
                f_c_min:    null   # floors_count_min
                f_c_max:    null   # floors_count_max
                p_c_min:    null   # persons_count_min
                p_c_max:    null   # persons_count_max
                t_a_min:    null   # total_area_min
                t_a_max:    null   # total_area_max
                f_min:      null   # floor_min
                f_max:      null   # floor_max
                h_a_min:    null   # halls_area_min
                h_a_max:    null   # halls_area_max
                c_c_min:    null   # cabinets_count_min
                c_c_max:    null   # cabinets_count_max
                h_c_min:    null   # halls_count_min
                h_c_max:    null   # halls_count_max
                c_h_min:    null   # ceiling_height_min
                c_h_max:    null   # ceiling_height_max
                a_min:      null   # area_min
                a_max:      null   # area_max

                # checkboxes
                n_b:    true   # new_buildings
                s_m:    true   # secondary_market
                fml:    false  # family
                frg:    false  # foreigners
                elt:    false  # electricity
                gas:    false  # gas
                h_w:    false  # hot_water
                c_w:    false  # cold_water
                swg:    false  # sewerage
                lft:    false  # lift
                sct:    false  # security
                ktn:    false  # kitchen
                s_a:    false  # security_alarm
                f_a:    false  # fire_alarm
                pit:    false  # pit
                wtr:    false  # water
                msd:    true   # mansard
                grd:    true    # ground

            panels:
                red:
                    r_t_sid: 1
                    r_op_sid:     0  # operation_sid
                    r_cu_sid:     1  # currency_sid
                    r_h_t_sid:    'false'  # heating_type_sid
                    r_pr_sid:     true  # period_sid
                    r_pl_sid:     'true'  # planing_sid
                    r_bg_t_sid:   false  # building_type_sid
                blue:
                    b_t_sid: null
                green:
                    g_t_sid: null
                yellow:
                    y_t_sid: null



    updateUrlFromFilters: ->
        filters = @filters
        searchParameters = ''

        for panel, panelFilters of filters.panels
            panelPrefix = panel.substring(0, 1)

            for filter, value of panelFilters
                type_sid = panelPrefix + '_t_sid'

                # Якщо фільтр це переметр з типом обєкта і його значення null
                # то переходимо до наступної ітерації
                if filter is type_sid and value is null then continue

                # Якщо значення фільтра null або пуста строка
                # то переходимо до наступної ітерації
                if value is null or value is '' then continue

                # Якщо значення фільтра таке ж саме як і значення в базовому наборі для даного фільтра
                # то переходимо до наступної ітерації
                if value is filters.base[filter.substring(2)] then continue

                searchParameters += (if searchParameters then '&' else '') + filter + '=' + value


#        console.log(@base64.urlencode(searchParameters))
#        @location.search(@base64.urlencode(searchParameters));




    ###*
    # @public
    # @description Formatted string from filters for loading markers
    #
    # @param {object} filters   - Filters of BFiltersService.filters
    # @returns {string}         - String filters
    ###
    createFiltersStringForLoadMarkers: () ->
        formattedFiltersObject =
            zoom:       @filters.map.z
            viewport:   @_createFormattedViewportForLoadingMarkers()
            filters:    []

        for panel in @filters.panels
            prefix = panel.substring(0, 1) + '_'

            if filters[panel][prefix + 't_sid']?
                formattedPanelFilters =
                    panel: panel

                _.each filters[panel], (value, key) ->
                    formattedPanelFilters[key.substring 2] = value if value? and value isnt false

                formattedFiltersObject.filters.push formattedPanelFilters

        JSON.stringify formattedFiltersObject



    ###*
    # @private
    # @description Create formatted viewport for filters string
    #
    # @returns {object} - Formatted viewport
    ###
    _createFormattedViewportForLoadingMarkers: ->
        sneLat = @filters.map.v.getNorthEast().lat().toString()
        sneLng = @filters.map.v.getNorthEast().lng().toString()
        sswLat = @filters.map.v.getSouthWest().lat().toString()
        sswLng = @filters.map.v.getSouthWest().lng().toString()

        neLat = sneLat.replace(sneLat.substring(sneLat.indexOf(".") + 3, sneLat.length), "")
        neLng = sneLng.replace(sneLng.substring(sneLng.indexOf(".") + 3, sneLng.length), "")
        swLat = sswLat.replace(sswLat.substring(sswLat.indexOf(".") + 3, sswLat.length), "")
        swLng = sswLng.replace(sswLng.substring(sswLng.indexOf(".") + 3, sswLng.length), "")

        'ne_lat': neLat
        'ne_lng': neLng
        'sw_lat': swLat
        'sw_lng': swLng




angular
    .module('mappino.pages.map')
    .factory('MFiltersService', ['$http', '$location', 'base64', (http, location, base64) -> new MFiltersService(http, location, base64)])