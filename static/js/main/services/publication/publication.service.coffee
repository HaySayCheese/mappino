'use strict'

###*
# @class
# @description todo: add desc
# @version 0.1.0
# @license todo: add license
###
class MPublicationService
    constructor: (@http) ->
        @publication=
            'data':     null
            'contacts': null
            'similar':  null


    ###*
    # @public
    # @description Load publication data by 'id:hash_id'
    #
    # @param {string} id_part               - Publication type_id:hash_id
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    getPublicationData: (id_part, successCallback, errorCallback) ->
        self = @
        @publication.data = null
        request = @http.get "/ajax/api/detailed/publication/#{id_part}/"

        request.success (response) ->
            #if response.code is 0
            self.publication.data = response
            _.isFunction(successCallback) && successCallback response
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Load publication contacts by 'id:hash_id'
    #
    # @param {string} id_part               - Publication type_id:hash_id
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    getPublicationContacts: (id_part, successCallback, errorCallback) ->
        self = @
        @publication.contacts = null
        request = @http.get "/ajax/api/detailed/publication/#{id_part}/contacts/"

        request.success (response) ->
            if response.code is 0
                self.publication.contacts = response
                _.isFunction(successCallback) && successCallback response
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Load similar publication by 'id:hash_id'
    #
    # @param {string} id_part               - Publication type_id:hash_id
    # @param {function()} [successCallback] - Success callback
    # @param {function()} [errorCallback]   - Error callback
    ###
    getPublicationSimilar: (id_part, successCallback, errorCallback) ->
        self = @
        @publication.similar = null
        request = @http.get "/ajax/api/detailed/publication/#{id_part}/similar/"

        request.success (response) ->
            if response.code is 0
                self.publication.similar = response
                _.isFunction(successCallback) && successCallback response
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Seller call request
    #
    # @param {string} id_part                           - Publication type_id:hash_id
    # @param {object} merchant                          - Merchant object
    # @param {string} merchant.name                     - Merchant name
    # @param {(string|number)} merchant.phone_number    - Merchant phone number
    # @param {function()} [successCallback]             - Success callback
    # @param {function()} [errorCallback]               - Error callback
    ###
    sendCallRequestToSeller: (id_part, merchant, successCallback, errorCallback) ->
        request = @http.post "/ajax/api/notifications/send-call-request/#{id_part}/",
            merchant

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback response
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()



    ###*
    # @public
    # @description Seller call request
    #
    # @param {string} id_part                           - Publication type_id:hash_id
    # @param {object} merchant                          - Merchant object
    # @param {string} merchant.name                     - Merchant name
    # @param {(string|number)} merchant.phone_number    - Merchant phone number
    # @param {function()} [successCallback]             - Success callback
    # @param {function()} [errorCallback]               - Error callback
    ###
    sendMessageToSeller: (id_part, merchant, successCallback, errorCallback) ->
        request = @http.post "/ajax/api/notifications/send-message/#{id_part}/",
            merchant

        request.success (response) ->
            if response.code is 0
                _.isFunction(successCallback) && successCallback response
            if response.code isnt 0
                _.isFunction(errorCallback) && errorCallback
                    'code': response.code

        request.error -> _.isFunction(errorCallback) && errorCallback()




angular
    .module('mappino.pages.map')
    .factory 'MPublicationService', ['$http', (http) -> new MPublicationService(http)]