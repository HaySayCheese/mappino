/**
 * Директива яка ставить фокус на поле введення
 **/
app.directive('focusOnLoad', function ($timeout) {
    return function (scope, element, attrs) {
        $timeout(function (){
            element.focus();
        }, 500);
    };
});