/**
 * Директива ибору текста в полі введення при кліку
 **/
app.directive('selectOnClick', function () {

    var i = 0;

    return function (scope, element, attrs) {
        element.bind('click', function () {

            i % 2 == 0 ? this.select() :
                document.selection ? document.selection.empty() : window.getSelection().removeAllRanges();

            i++;
        });
    };
});