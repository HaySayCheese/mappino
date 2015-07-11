/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class UnpublishedPublicationController {
        private _publication: Object = {};

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: angular.ui.IStateService,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            this._publication['tid']    = $state.params['id'].split(':')[0];
            this._publication['hid']    = $state.params['id'].split(':')[1];

            $scope.publication = {};


            this.loadPublicationData();
        }



        private uploadPhoto($file, $event, $flow) {
            console.log($file)
        }



        private loadPublicationData() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadPublication(this._publication, (response) => {
                this.$scope.publication = response;
                this.$rootScope.loaders.base = false;

                this.initInputsChange();
            });
        }



        private initInputsChange() {
            angular.element("form[name='publicationForm'] input, form[name='publicationForm'] textarea").bind("focusout", (e) => {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.publicationForm[name].$dirty) {
                    return;
                }

                this.publicationsService.checkField(this._publication, { f: name, v: value }, (newValue) => {
                    if (newValue && !angular.element(e.currentTarget).is(":focus")) {
                        e.currentTarget['value'] = newValue;
                    }

                    this.$scope.publicationForm[name].$setValidity("invalid", true);
                }, (response) => {
                    this.$scope.publicationForm[name].$setValidity("invalid", response.code === 0);
                });
            });

            angular.element(".publication-view-container input[type='checkbox']").bind("change", function(e) {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['checked'];

                this.publicationsService.checkField(this._publication, { f: name, v: value });
            });
        }


        private checkField(elementName) {
            var elementValue = null;

            this.validatePublicationOperation();

            if (elementName.indexOf('rent_') !== -1) {
                elementValue = this.$scope.publication.rent_terms[elementName.replace('rent_', '')];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (elementName.indexOf('sale_') !== -1) {
                elementValue = this.$scope.publication.sale_terms[elementName.replace('sale_', '')];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.head[elementName])) {
                elementValue = this.$scope.publication.head[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.body[elementName])) {
                elementValue = this.$scope.publication.body[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.rent_terms[elementName])) {
                elementValue = this.$scope.publication.rent_terms[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.sale_terms[elementName])) {
                elementValue = this.$scope.publication.sale_terms[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });
            }
        }



        private validatePublicationOperation() {
            if (this.$scope.publication.head.for_sale == false && this.$scope.publication.head.for_rent == false) {
                this.$scope.publication.head.for_sale = true;
                this.checkField('for_sale');
            }
        }
    }
}