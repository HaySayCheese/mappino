/**
 * Директива ибору текста в полі введення при кліку
 **/
app.directive('selectOnClick', function () {
    return function (scope, element, attrs) {
        element.bind('click', function () {
            if (this.selectionEnd == this.selectionStart)
                this.select();
        });
    };
});