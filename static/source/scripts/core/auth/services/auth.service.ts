module mappino.core.auth {

    export class AuthService implements IAuthService {
        private _user: IUser = {
            account: {
                first_name:         null,
                last_name:          null,
                full_name:          null,
                avatar_url:         null,
                add_landline_phone: null,
                add_mobile_phone:   null,
                email:              null,
                landline_phone:     null,
                mobile_phone:       null,
                skype:              null,
                work_email:         null,
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



        public checkPhoneNumber(phoneNumber: string, success?: Function, error?: Function) {
            this.$http.post('/ajax/api/accounts/login/', {
                "phone_number": phoneNumber
            }).then((response) => {
                if (response.data['code'] === 0) {
                    _.isFunction(success) && success(response.data)
                } else {
                    _.isFunction(error) && error(response.data)
                }
            }, (response) => {
                _.isFunction(error) && error(response.data)
            });
        }



        public checkSMSCode(phoneNumber: string, smsCode: string, success?: Function, error?: Function) {
            this.$http.post('/ajax/api/accounts/login/check-code/', {
                "phone_number": phoneNumber,
                "token":        smsCode
            }).then((response) => {
                if (response.data['code'] === 0) {
                    this.updateProfileField(response.data['data']);
                    this.$cookies.remove('mcheck');
                    _.isFunction(success) && success(response.data)
                } else {
                    this.clearUserFromStorage();
                    _.isFunction(error) && error(response.data)
                }
            }, (response) => {
                this.clearUserFromStorage();
                _.isFunction(error) && error(response.data)
            });
        }




        public tryLogin(success?: Function, error?: Function) {
            this.$http.get('/ajax/api/accounts/on-login-info/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.updateProfileField(response.data['data']);
                        _.isFunction(success) && success(response.data)
                    } else {
                        this.clearUserFromStorage();
                        _.isFunction(error) && error(response.data)
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data)
                })
        }



        public loadProfile(success?, error?) {
            this.$http.get('/ajax/api/cabinet/account/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        this.updateProfileField(response.data['data']['account']);
                        this.updateProfileField(response.data['data']['preferences']);

                        _.isFunction(success) && success(this._user);
                    } else {
                        _.isFunction(error) && error(response.data);
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data);
                });
        }



        public checkProfileField(field: Object, success?, error?) {
            this.$http.post('/ajax/api/cabinet/account/', field)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        field['v'] = response.data['value'] ? response.data['value'] : field['v'];

                        var _field = {};
                        _field[field['f']] = field['v'];

                        this.updateProfileField(_field);
                        _.isFunction(success) && success(field['v']);
                    } else {
                        _.isFunction(error) && error(response.data);
                    }
                }, (response) => {
                    _.isFunction(error) && error(response.data);
                })
        }



        public uploadAvatar(avatar: File, success?, error?) {
            this.Upload.upload({
                url: '/ajax/api/cabinet/account/photo/',
                file: avatar
            }).success((response) => {
                if (response.code === 0) {
                    this.updateProfileField({ avatar_url: response.data['url'] });
                    _.isFunction(success) && success(response);
                } else {
                    _.isFunction(error) && error(response)
                }
            }).error((response) => {
                _.isFunction(error) && error(response)
            })
        }



        public removeAvatar(success?, error?) {
            this.$http.delete('/ajax/api/cabinet/account/photo/')
                .then((response) => {
                    _.isFunction(success) && success(response);
                }, (response) => {
                    _.isFunction(error) && error(response)
                })
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