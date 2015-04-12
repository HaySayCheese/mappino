angular.module '_modules.bDirectives', ['underscore']
    ##
    # Allow only number directive
    ##
    .directive 'allowOnlyNumber', ['_', (_) ->
        (scope, element, attrs) ->
            keyCode = [8,9,37,39,48,49,50,51,52,53,54,55,56,57,96,97,98,99,100,101,102,103,104,105,110]

            element.bind 'keydown', (event) ->
                if _.indexOf(keyCode, event.which) is -1
                    scope.$apply () ->
                        scope.$eval attrs.onlyNum
                        event.preventDefault()
                    event.preventDefault()
    ]



    ##
    # jQuery image scroll (parallax) directive
    ##
    .directive 'imageScroll', ['$timeout', ($timeout) ->
        restrict: 'A'

        link: (scope, element) ->
            $timeout () ->
                angular.element(element).imageScroll
                    container: $('.wrapper')
                    touch: Modernizr.touch
    ]



    ##
    # jQuery selectpicker (dropdown) directive
    ##
    .directive 'selectpicker', ['$timeout', ($timeout) ->
        restrict: 'A'

        link: (scope, element) ->
            $timeout () ->
                angular.element(element).selectpicker
                    style: 'btn-default btn-md'
                    container: angular.element 'body'
    ]



    ##
    # jQuery perfectScrollbar (scroll) directive
    ##
    .directive 'perfectScrollbar', ['$timeout', '$rootScope', ($timeout, $rootScope) ->
        restrict: 'A'

        link: (scope, element) ->
            $timeout () ->
                angular.element(element).perfectScrollbar
                    wheelSpeed: 20
                    useKeyboard: false

            angular.element(window).resize () ->
                angular.element(element).perfectScrollbar 'update'

            $rootScope.$on 'updatePerfectScrollbar', () ->
                $timeout () ->
                    angular.element(element).perfectScrollbar 'update'
                , 50
    ]