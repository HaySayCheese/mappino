'use strict'

###*
# @class
# @description todo: add desc
# @version 0.0.1
# @license todo: add license
###
class MMarkersService
    constructor: (@http, @filtersService) ->


    load: () ->
        @filtersService.updateUrlFromFilters()



    ###*
    # @private
    # @description Create request filters object
    #
    # @param {object} filters   - Filters of BFiltersService.filters
    # @returns {string}         - String filters
    ###




angular
    .module('mappino.pages.map')
    .factory('MMarkersService', ['$http', 'MFiltersService', (http, filtersService) -> new MMarkersService(http, filtersService)])