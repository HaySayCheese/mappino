// Generated by CoffeeScript 1.9.2
(function() {
  var app;

  app = angular.module('mappino.pages.map', ['ngRoute', 'ngCookies', 'ngAnimate', 'ngResource', 'ui.mask', 'lrNotifier', 'ab-base64', 'underscore', '_modules.bTypes', '_modules.bAuth', '_modules.bDirectives']);

  app.config([
    '$interpolateProvider', '$locationProvider', function(interpolateProvider, locationProvider) {
      interpolateProvider.startSymbol('[[');
      interpolateProvider.endSymbol(']]');
      return locationProvider.hashPrefix('!');
    }
  ]);

  app.config([
    '$resourceProvider', function(resourceProvider) {
      return resourceProvider.defaults.stripTrailingSlashes = false;
    }
  ]);

  app.run([
    '$http', '$cookies', function(http, cookies) {
      return http.defaults.headers.common['X-CSRFToken'] = cookies.csrftoken;
    }
  ]);

}).call(this);

//# sourceMappingURL=app.js.map
