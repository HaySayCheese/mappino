app.factory('CurrencyTypesFactory', function() {
    "use strict";

    var currencyTypes = [{
        id: 0,
        name: "USD",
        title: "Дол."
    }, {
        id: 1,
        name: "EUR",
        title: "Евро"
    }, {
        id: 2,
        name: "UAH",
        title: "Грн."
    }];

    return {
        getCurrencyTypes: function() {
            return currencyTypes;
        }
    };
});