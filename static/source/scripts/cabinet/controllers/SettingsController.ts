/// <reference path='../_references.ts' />


module pages.cabinet {
    export class SettingsController {

        public static $inject = [
            '$scope',
            '$timeout',
            'SettingsService'
        ];

        constructor(
            private $scope: any,
            private $timeout: angular.ITimeoutService,
            private settingsService: bModules.Auth.SettingsService) {
            // -
            $scope.settingsIsLoaded = false;

            $timeout(() => $('select').material_select());


            this.initInputsChange();


            settingsService.load((response) => {
                $scope.user = response;
                $scope.settingsIsLoaded = true;
                $timeout(() => {
                    angular.element(".settings-page input:not([type='file'], [type='checkbox'])").change()
                });
            });
        }



        private changePhoto(event) {
            event.preventDefault();

            angular.element('#photo-field').click();
        }



        private initInputsChange() {
            var self = this;

            angular.element(".settings-page input[type='file']").bind('change', (event) => {
                self.settingsService.uploadAvatar(event.target['files'][0], (response) => {
                    self.$scope.imageFatal      = response.code === 1;
                    self.$scope.imageTooLarge   = response.code === 2;
                    self.$scope.ImageTooSmall   = response.code === 3;
                    self.$scope.ImageUndefined  = response.code === 4;
                });
            });

            angular.element(
                ".settings-page input[type='text'], " +
                ".settings-page input[type='tel'], " +
                ".settings-page input[type='email']")
                .bind("focusout", (e) => {
                // -
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!self.$scope.form.user[name].$dirty)
                    return;

                if (name === "mobile_phone" && (value === "+38 (0__) __ - __ - ___" || value[22] === "_"))
                    return;

                self.settingsService.check({ f: name, v: value }, (newValue, code) => {
                    console.log(newValue)
                    console.log(code)
                    if (newValue)
                        e.currentTarget['value'] = newValue;

                    self.$scope.form.user[name].$setValidity("incorrect", code !== 10);
                    self.$scope.form.user[name].$setValidity("duplicated", code !== 11);
                });

            });

            angular.element(".settings-page input[type='checkbox']").bind("change", (e) => {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['checked'];

                self.settingsService.check({ f: name, v: value }, null);
            });
            //
            //angular.element(".sidebar-item-detailed-body select").bind('change',function(e) {
            //    var name  = e.currentTarget.name,
            //        value = e.currentTarget.value;
            //
            //    Settings.checkInputs({ f: name, v: value }, null);
            //});
        }
    }
}