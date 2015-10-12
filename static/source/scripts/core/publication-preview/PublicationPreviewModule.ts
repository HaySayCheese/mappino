namespace Mappino.Core.PublicationPreview {

    import IModule = angular.IModule;

    "use strict";


    var publicationPreviewModule: IModule = angular.module('Mappino.Core.PublicationPreview', [
        'ngMaterial'
    ]);

    publicationPreviewModule.service('PublicationPreviewService', PublicationPreviewService);

    publicationPreviewModule.filter('capitalize', CapitalizeFilter);

    publicationPreviewModule.controller('PublicationPreviewController', PublicationPreviewController);

    publicationPreviewModule.directive('publicationPreview', PublicationPreviewDirective);
    publicationPreviewModule.directive('publicationPreviewHeader', PublicationPreviewHeaderDirective);
    publicationPreviewModule.directive('publicationPreviewBody', PublicationPreviewBodyDirective);
    publicationPreviewModule.directive('publicationPreviewContacts', PublicationPreviewContactsDirective);
    publicationPreviewModule.directive('publicationPreviewError', PublicationPreviewErrorDirective);

}