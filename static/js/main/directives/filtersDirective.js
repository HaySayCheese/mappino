"use strict";

app.directive('fCheckboxes', function () {
    return {
        restrict: 'A',

        link: function (scope, element) {

            var checkboxes = {
                    red:    false,
                    blue:   false,
                    green:  false,
                    yellow: false
                };

            var checkboxesElements = angular.element($("[f-checkboxes] [f-checkbox]"));


            checkboxesElements.on("click", function(e) {
                var el = e.currentTarget,
                    parent = angular.element(el).parent();

                if (el.checked) {
                    for (var c in checkboxes) {
                        if (!checkboxes[c] && checkboxes.hasOwnProperty(c)) {
                            checkboxes[c] = true;

                            parent.addClass(c);
                            parent.find("input").attr("checked", "checked");

                            return;
                        }
                    }
                } else {
                    var suggestsCheckboxes = $("[f-checkboxes] [f-checkbox][suggest]:checked");
                    suggestsCheckboxes.attr("checked", null).trigger("click");


                    var classes = parent.attr("class").split(/\s+/),
                        color = classes[classes.length - 1];

                    parent.removeClass(color);
                    parent.find("input").attr("checked", null);
                    checkboxes[color] = false;
                }
            });
        }
    };
});