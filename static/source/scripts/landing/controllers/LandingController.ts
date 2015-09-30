namespace Mappino.Landing {
    export class LandingController {

        public static $inject = [
            '$scope'
        ];

        constructor(private $scope: any) {
            // ---------------------------------------------------------------------------------------------------------
            $scope.search = {
                realty_type_sid: 0,
                operation_sid: 0
            }
        }
    }
}