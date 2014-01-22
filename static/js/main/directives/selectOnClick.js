/**
 * Директива ибору текста в полі введення при кліку
 **/
app.directive('selectOnClick', function () {
    return function (scope, element, attrs) {
        element.bind('click', function () {
            this.select();
        });
    };
});