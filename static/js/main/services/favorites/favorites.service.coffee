'use strict'

###*
# @class
# @description todo: add desc
# @version 0.1.0
# @license todo: add license
###
class MFavoritesService
    constructor: (@http) ->
        @bookmarks = []


    ###*
    # @public
    # @description Add publication to favorites
    #
    # @param {(string|number)} tid              - Publication type id
    # @param {(string|number)} hid              - Publication hash id
    # @param {function()} [successCallback]     - Success callback
    # @param {function()} [errorCallback]       - Error callback
    ###
    add: (tid, hid, successCallback, errorCallback) ->
        request = @http.post "/ajax/api/favorites/",
            'tid': tid
            'hid': hid

        request.success (response) ->
            if response.code is 0
#                self._saveInStorage response.user
                _.isFunction(successCallback) && successCallback()
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()





angular
    .module('mappino.pages.map')
    .factory 'MFavoritesService', ['$http', (http) -> new MFavoritesService(http)]