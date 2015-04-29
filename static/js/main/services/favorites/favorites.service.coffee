'use strict'

###*
# @class
# @description todo: add desc
# @version 0.1.0
# @license todo: add license
###
class MFavoritesService
    constructor: (@resource) ->
        @favorites = @resource "/ajax/api/favorites/", null,
            add:    method: "POST"
            get:    method: "GET"
            remove: method: "DELETE"



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
        request = @favorites.add
            'tid': tid
            'hid': hid


        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            () -> _.isFunction(errorCallback) && errorCallback()
        )



    ###*
    # @public
    # @description Get all favorites
    #
    # @param {(string|number)} tid              - Publication type id
    # @param {(string|number)} hid              - Publication hash id
    # @param {function()} [successCallback]     - Success callback
    # @param {function()} [errorCallback]       - Error callback
    ###
    get: (tid, hid, successCallback, errorCallback) ->
        request = @favorites.get
            params:
                'tid': tid
                'hid': hid

        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            () -> _.isFunction(errorCallback) && errorCallback()
        )



    ###*
    # @public
    # @description Remove publication from favorites
    #
    # @param {(string|number)} tid              - Publication type id
    # @param {(string|number)} hid              - Publication hash id
    # @param {function()} [successCallback]     - Success callback
    # @param {function()} [errorCallback]       - Error callback
    ###
    remove: (tid, hid, successCallback, errorCallback) ->
        request = @favorites.remove
            params:
                'tid': tid
                'hid': hid

        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            () -> _.isFunction(errorCallback) && errorCallback()
        )





angular
    .module('mappino.pages.map')
    .factory 'MFavoritesService', ['$resource', (resource) -> new MFavoritesService(resource)]