'use strict'

###*
# @class
# @description todo: add desc
# @version 0.0.1
# @license todo: add license
###
class MRouterService
    constructor: (routeProvider, ROUTES) ->
        routeProvider
            .when ROUTES.SEARCH.URL,
                templateUrl:    ROUTES.SEARCH.TEMPLATE
                reloadOnSearch: false

            .when ROUTES.REALTOR.URL,
                templateUrl:    ROUTES.REALTOR.TEMPLATE
                reloadOnSearch: false

            .when ROUTES.LOGIN.URL,
                templateUrl:    ROUTES.LOGIN.TEMPLATE
                reloadOnSearch: false

            .when ROUTES.REGISTRATION.URL,
                templateUrl:    ROUTES.REGISTRATION.TEMPLATE
                reloadOnSearch: false

            .when ROUTES.RESTORE_ACCESS.URL,
                templateUrl:    ROUTES.RESTORE_ACCESS.TEMPLATE
                reloadOnSearch: false

            .when ROUTES.PUBLICATION.URL,
                templateUrl:    ROUTES.PUBLICATION.TEMPLATE
                reloadOnSearch: false

            .otherwise
                redirectTo: ROUTES.SEARCH.URL



mappinoMapModule = angular.module 'mappino.pages.map'
mappinoMapModule.config ['$routeProvider', 'ROUTES',
    (routeProvider, ROUTES) -> new MRouterService(routeProvider, ROUTES)]
