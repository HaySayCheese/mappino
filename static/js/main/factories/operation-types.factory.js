app.factory('OperationTypesFactory', function() {
    "use strict";

    var operationTypes = [{
        id: 0,
        name: 'sale',
        title: 'Продажа'
    } , {
        id: 1,
        name: 'rent',
        title: 'Аренда'
    }];

    return {
        getOperationTypes: function() {
            return operationTypes;
        }
    };
});