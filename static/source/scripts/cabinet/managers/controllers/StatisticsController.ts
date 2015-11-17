namespace Mappino.Cabinet.Managers {
    export class StatisticsController {

        public static $inject = [
            '$scope',
            '$rootScope',
            'ManagingService'
        ];


        constructor(private $scope: any,
                    private $rootScope: any,
                    private managingService: ManagingService) {
            // ---------------------------------------------------------------------------------------------------------
            $rootScope.pageTitle = 'Статистика mappino';
            this.getStatistics();

        }


        public getStatistics() {
            this.$rootScope.loaders.overlay = true;

            this.managingService.getStatistics()
                .success(response => {
                    this.$rootScope.loaders.overlay = false;

                    this.$scope.statistics = response.data;
                });
        }


    }
}