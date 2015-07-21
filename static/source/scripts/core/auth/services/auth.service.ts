module Mappino.Core.Auth {

    export class AuthService implements IAuthService {
        private _user: IUser = {
            account: {
                first_name:         null,
                last_name:          null,
                full_name:          null,
                avatar_url:         null,
                mobile_code:        '+380',
                mobile_phone:       null,
                add_mobile_code:    '+380',
                add_mobile_phone:   null,
                landline_phone:     null,
                add_landline_phone: null,
                email:              null,
                skype:              null,
                work_email:         null
            },
            preferences: {
                allow_call_requests:            true,
                allow_messaging:                true,
                hide_add_landline_phone_number: true,
                hide_add_mobile_phone_number:   true,
                hide_email:                     true,
                hide_landline_phone_number:     true,
                hide_mobile_phone_number:       true,
                hide_skype:                     true,
                send_call_request_notifications_to_sid: 0,
                send_message_notifications_to_sid:      0
            }
        };

        public static $inject = [
            '$http',
            '$cookies',
            'Upload'
        ];


        constructor(private $http: angular.IHttpService,
                    private $cookies: angular.cookies.ICookiesService,
                    private Upload: any) {
            // ---------------------------------------------------------------------------------------------------------
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
                    this.updateProfileField(response.data['data']);
                    this.$cookies.remove('mcheck');
                    angular.isFunction(successCallback) && successCallback(response.data)
                } else {
                    this.clearUserFromStorage();
                    angular.isFunction(errorCallback) && errorCallback(response.data)
                }
            }, response => {
                this.clearUserFromStorage();
                angular.isFunction(errorCallback) && errorCallback(response.data)
            });
        }




        public tryLogin(successCallback?, errorCallback?) {
            this.$http.get(`/ajax/api/accounts/on-login-info/`)
                .then(response => {
                    if (response.data['code'] === 0) {
                        this.updateProfileField(response.data['data']);
                        angular.isFunction(successCallback) && successCallback(response.data)
                    } else {
                        this.clearUserFromStorage();
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
                        this.updateProfileField(response.data['data']['account']);
                        this.updateProfileField(response.data['data']['preferences']);

                        angular.isFunction(successCallback) && successCallback(this._user);
                    } else {
                        angular.isFunction(errorCallback) && errorCallback(response.data);
                    }
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response.data);
                });
        }



        public checkProfileField(field, successCallback?, errorCallback?) {
            var fullMobileNumber = {
                fieldName:  field.fieldName,
                fieldValue: null
            };

            if (field.fieldName == 'mobile_phone') {
                fullMobileNumber = {
                    fieldName:  field.fieldName,
                    fieldValue: this._user.account.mobile_code + field.fieldValue
                };
            }

            if (field.fieldName == 'add_mobile_phone') {
                fullMobileNumber = {
                    fieldName:  field.fieldName,
                    fieldValue: this._user.account.add_mobile_code + field.fieldValue
                }
            }

            this.$http.post(`/ajax/api/cabinet/account/`, fullMobileNumber.fieldValue ? fullMobileNumber : field)
                .then(response => {
                    if (response.data['code'] === 0) {
                        field['fieldValue'] = response.data['value'] ? response.data['value'] : field['fieldValue'];

                        var _field = {};
                        _field[field['fieldName']] = field['fieldValue'];

                        this.updateProfileField(_field);
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
                    this.updateProfileField({ avatar_url: response.data['url'] });
                    angular.isFunction(successCallback) && successCallback(response);
                } else {
                    angular.isFunction(errorCallback) && errorCallback(response)
                }
            }, response => {
                angular.isFunction(errorCallback) && errorCallback(response)
            })
        }



        public removeAvatar(successCallback?, errorCallback?) {
            this.$http.delete(`/ajax/api/cabinet/account/photo/`)
                .then(response => {
                    this.updateProfileField({ avatar_url: null });
                    angular.isFunction(successCallback) && successCallback(this._user);
                }, response => {
                    angular.isFunction(errorCallback) && errorCallback(response)
                });
        }



        private updateProfileField(params: Object) {
            for (var key in params) {
                if (this._user.account[key] !== undefined) {
                    this._user.account[key] = params[key];

                    if (key === 'first_name' || key === 'last_name') {
                        this._user.account.full_name = this._user.account.first_name + ' ' + this._user.account.last_name;
                    }
                }

                if (this._user.preferences[key] != undefined) {
                    this._user.preferences[key] = params[key];
                }
            }
            this.saveUserToStorage(this._user);
        }



        public get user() {
            return this._user;
        }



        private clearUserFromStorage() {
            if (localStorage && localStorage['user']) {
                delete localStorage['user']
            }
        }



        private saveUserToStorage(user: Object) {
            if (localStorage) {
                localStorage['user'] = JSON.stringify(user);
            }
        }
    }
}