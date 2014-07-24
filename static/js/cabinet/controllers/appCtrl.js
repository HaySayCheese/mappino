'use strict';

app.controller('AppCtrl', function($scope, $rootScope, $routeParams, $location, Settings) {

    Object.defineProperty(console, '_commandLineAPI', {
        get : function() {
            throw 'Kein Zugriff!'
        }
    });

    $rootScope.publicationsCount = {
        all: 0,
        published: 0,
        unpublished: 0,
        trash: 0
    };

    $rootScope.pageTitle = "Mappino";

    /**
     * Лоадери
     */
    $rootScope.loadings = {
        tags:           false,
        briefs:         false,
        detailed:       false,
        settings:       false,
        support:        false,
        tickets:        false,
        ticketData:     false,
        uploadPhotos:   false,
        chartData:      false
    };


    /**
     * Перегляд за зміною урла для встановлення активного
     * пункту меню
     */
    $scope.$on("$routeChangeSuccess", function() {
        $rootScope.routeBase            = "";
        $rootScope.routeSection         = "";
        $rootScope.publicationId        = "";
        $rootScope.isSupportPagePart    = false;

        if ($location.path().replace("/", ""))
            $rootScope.routeBase = $location.path().replace("/", "");


        if ($routeParams.section) {
            $rootScope.routeSection = $routeParams.section;

            if ($rootScope.routeSection == "all") {
                $rootScope.pageTitle = "Все обьявления - Mappino";
                ga('send', 'pageview', {
                    'page': '/cabinet/#!/publication/all',
                    'title': $rootScope.pageTitle
                });
            }

            else if ($rootScope.routeSection == "published") {
                $rootScope.pageTitle = "Опубликованные обьявления - Mappino";
                ga('send', 'pageview', {
                    'page': '/cabinet/#!/publication/published',
                    'title': $rootScope.pageTitle
                });
            }

            else if ($rootScope.routeSection == "unpublished") {
                $rootScope.pageTitle = "Неопубликованные обьявления - Mappino";
                ga('send', 'pageview', {
                    'page': '/cabinet/#!/publication/unpublished',
                    'title': $rootScope.pageTitle
                });
            }

            else if ($rootScope.routeSection == "trash") {
                $rootScope.pageTitle = "Удаленные обьявления - Mappino";
                ga('send', 'pageview', {
                    'page': '/cabinet/#!/publication/trash',
                    'title': $rootScope.pageTitle
                });
            }

            else {
                $rootScope.pageTitle = $rootScope.routeSection + " - Mappino";
                ga('send', 'pageview', {
                    'page': '/cabinet/#!/publication/' + $rootScope.routeSection,
                    'title': $rootScope.pageTitle
                });
            }
        }


        if ($routeParams.pubId) {
            $rootScope.publicationId = $routeParams.pubId;
            ga('send', 'pageview', {
                'page': '/cabinet/#!/publication/' + $rootScope.routeSection + '/' + $rootScope.publicationId,
                'title': $rootScope.pageTitle
            });
        }

        if ($routeParams.ticketId)
            $rootScope.isSupportPagePart = true;

    });

    /**
     *  Вихід з адмінки
     */
    $rootScope.logoutFromCabinet = function() {
        Settings.logoutUser();
    };


    angular.element(document).ready(function() {
        setTimeout(function() {
            angular.element(".wrapper").addClass("fadeInDown")
        }, 100)

    });
});