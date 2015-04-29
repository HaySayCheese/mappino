app = angular.module('mappino.pages.map', [
    'ngRoute'
    'ngCookies'
    'ngAnimate'
    'ngResource'

    'ui.mask'
    'lrNotifier'
    'ab-base64'

    'underscore'

    '_modules.bTypes'
    '_modules.bAuth'
    '_modules.bDirectives'
])


app.config(['$interpolateProvider', '$locationProvider',
    (interpolateProvider, locationProvider) ->
        interpolateProvider.startSymbol '[['
        interpolateProvider.endSymbol ']]'

        locationProvider.hashPrefix '!'
])

app.config(['$resourceProvider', (resourceProvider) ->
    resourceProvider.defaults.stripTrailingSlashes = false
])


app.run(['$http', '$cookies',
    (http, cookies) ->
        http.defaults.headers.common['X-CSRFToken'] = cookies.csrftoken
])