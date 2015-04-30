'use strict'

###*
# @class
# @description todo: add desc
# @version 0.1.0
# @license todo: add license
###
class MFavoritesService
    constructor: (@$resource) ->
        @favorites = @$resource "/ajax/api/favorites/:id"



    ###*
    # @public
    # @description Add publication to favorites
    #
    # @param {string} pid                   - Publication id ('tid:hid') as string
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    add: (pid, successCallback, errorCallback) ->
        request = @favorites.save 'id': pid

        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            (response) -> _.isFunction(errorCallback) && errorCallback()
        )



    ###*
    # @public
    # @description Get all favorites
    #
    # @param {function()} [successCallback]     - Success callback
    # @param {function()} [errorCallback]       - Error callback
    ###
    get: (successCallback, errorCallback) ->
        request = @favorites.query()

        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            (response) -> _.isFunction(errorCallback) && errorCallback()
        )



    ###*
    # @public
    # @description Remove publication from favorites
    #
    # @param {string} pid                   - Publication id ('tid:hid') as string
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    remove: (pid, successCallback, errorCallback) ->
        request = @favorites.remove 'id': pid

        request.$promise.then(
            (response) ->
                if response.code is 0
                    _.isFunction(successCallback) && successCallback()
                if response.code isnt 0
                    _.isFunction(errorCallback) && errorCallback
                        'code': response.code

            (response) -> _.isFunction(errorCallback) && errorCallback()
        )



# angular service create
angular
    .module('mappino.pages.map')
    .factory 'MFavoritesService', ['$resource', ($resource) -> new MFavoritesService($resource)]