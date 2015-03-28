app.factory('RentTypesFactory', function() {
    "use strict";

    var rentTypes = [{
        id: 0,
        name: "ignore",
        title: "Не учитывать"
    }, {
        id: 1,
        name: "daily",
        title: "Посуточно"
    }, {
        id: 2,
        name: "monthly",
        title: "Помесячно"
    }];

    return {
        getRentTypes: function() {
            return rentTypes;
        }
    };
});