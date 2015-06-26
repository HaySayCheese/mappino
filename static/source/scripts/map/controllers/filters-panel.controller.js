export class FiltersPanelController {
    constructor($scope, filtersService, realtyTypesService) {
    	this.$scope 		= $scope;
    	
        $scope.filters 		= filtersService.filters.panels;
        $scope.realtyTypes 	= realtyTypesService.realty_types;
    }
}

FiltersPanelController.$inject = ['$scope', 'FiltersService', 'RealtyTypesService'];