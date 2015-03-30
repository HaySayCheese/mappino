var app = app || angular.module("mappino.home", [
            'ngCookies',
            'ab-base64',
            'binno.utils.angular.services.user',

            'binno.utils.angular.directives.selectpicker',
            'binno.utils.angular.directives.imageScroll'
        ]
    );



app.config(['$interpolateProvider', function($interpolateProvider) {
    "use strict";

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);