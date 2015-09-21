namespace Mappino.Core.PublicationPreview {
    export function PublicationPreviewDirective(): ng.IDirective {
        return {
            restrict: 'E',
            controller: PublicationPreviewController,
            controllerAs: 'pubPreviewCtrl',
            templateUrl: '/ajax/template/common/publication-preview/container/',

            link: (scope, element, attrs, model: any) => {
                var $element = angular.element(element),
                    hiddenControls = [];

                if (angular.isDefined(attrs['hiddenControls'])) {
                    hiddenControls = attrs['hiddenControls'].split(' ');
                }

                model.$scope.pubPreviewCtrl.$scope.hiddenControls = {};

                for (let i = 0, len = hiddenControls.length; i < len; i++) {
                    var control = hiddenControls[i];

                    model.$scope.pubPreviewCtrl.$scope.hiddenControls[control] = true;
                }
            }
        }
    }
}