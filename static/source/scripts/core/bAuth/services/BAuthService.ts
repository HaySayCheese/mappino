namespace Mappino.Core.BAuth {

    export class BAuthService implements IBAuthService {
        private _user: User;

        public static $inject = [
            '$http',
            '$cookies',
            'Upload'
        ];


        constructor(private $http: angular.IHttpService,
                    private $cookies: angular.cookies.ICookiesService,
                    private Upload: any) {
            // ---------------------------------------------------------------------------------------------------------
            this._user = new User();
        }



        public checkPhoneNumber(phoneNumber: string, successCallback?: Function, errorCallback?: Function) {
            this.$http.post(`/ajax/api/accounts/login/`, {
                "phone_number": phoneNumber
            }).then(response => {
                if (response.data['code'] === 0) {
                    angular.isFunction(successCallback) && successCallback(response.data)
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                angular.isFunction(errorCallback) && errorCallback(response.data)
            });
        }



        public checkSMSCode(phoneNumber, smsCode, successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/accounts/login/check-code/`, {
                'phone_number': phoneNumber,
                'token':        smsCode
            }).then(response => {
                if (response.data['code'] === 0) {
                    this._user.set(response.data['data']);
                    this.$cookies.remove('mcheck');
                    angular.isFunction(successCallback) && successCallback(response.data)
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                angular.isFunction(errorCallback) && errorCallback(response.data)
            });
        }




        public tryLogin(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/accounts/on-login-info/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._user.set(response.data['data']);
                        angular.isFunction(successCallback) && successCallback(angular.copy(this._user))
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data)
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                })
        }



        public loadProfile(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/cabinet/account/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this._user.set(response.data['data']['account']);
                        this._user.set(response.data['data']['preferences']);

                        angular.isFunction(successCallback) && successCallback(angular.copy(this._user));
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data);
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data);
                });
        }



        public checkProfileField(field, successCallback?, errorCallback?) {
            var fullMobileNumber = {
                fieldName:  null,
                fieldValue: null
            };

            if (field.fieldName == 'mobile_phone') {
                fullMobileNumber = {
                    fieldName:  field.fieldName,
                    fieldValue: this._user.get().account.mobile_code + field.fieldValue
                };
            }

            if (field.fieldName == 'add_mobile_phone') {
                fullMobileNumber = {
                    fieldName:  field.fieldName,
                    fieldValue: this._user.get().account.add_mobile_code + field.fieldValue
                }
            }

            this.$http.post(`/ajax/api/cabinet/account/`, fullMobileNumber.fieldValue ? fullMobileNumber : field)
                .then(response => {
                    if (response.data['code'] === 0) {
                        field['fieldValue'] = response.data['value'] ? response.data['value'] : field['fieldValue'];

                        var _field = {};
                        _field[field['fieldName']] = field['fieldValue'];

                        this._user.set(_field);
                        angular.isFunction(successCallback) && successCallback(field['fieldValue']);
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data);
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data);
                })
        }



        public uploadAvatar(avatar, successCallback?, errorCallback?) {
            this.Upload.upload({
                url: `/ajax/api/cabinet/account/photo/`,
                file: avatar
            }).then(response => {
                if (response.data['code'] === 0) {
                    this._user.set({ avatar_url: response.data.data['url'] });
                    angular.isFunction(successCallback) && successCallback(response.data);
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                angular.isFunction(errorCallback) && errorCallback(response.data)
            })
        }




        public removeAvatar(successCallback?, errorCallback?) {
            this.$http.delete(`/ajax/api/cabinet/account/photo/`)
                .then(response => {
                    this._user.set({ avatar_url: null });
                    angular.isFunction(successCallback) && successCallback(this.user);
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response)
                });
        }



        public logout(successCallback?, errorCallback?) {
            this.$http.post(`/ajax/api/accounts/logout/`, null)
                .then(response => {
                    this.$cookies.remove('sessionid');
                    angular.isFunction(successCallback) && successCallback(response.data);
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                });
        }



        public get user() {
            return this._user.get();
        }
    }
}