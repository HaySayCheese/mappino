angular.module('mappino.directives.allowOnlyNumber', [])
    .directive('allowOnlyNumber', function () {
        return function(scope, element, attrs) {

            var keyCode = [8,9,37,39,48,49,50,51,52,53,54,55,56,57,96,97,98,99,100,101,102,103,104,105,110];

            element.bind("keydown", function(event) {

                if($.inArray(event.which, keyCode) == -1) {
                    scope.$apply(function(){
                        scope.$eval(attrs.onlyNum);
                        event.preventDefault();
                    });

                    event.preventDefault();
                }

            });
        };
});