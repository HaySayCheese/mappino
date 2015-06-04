/// <reference path='../_references.ts' />


module bModules.Auth {

    export class SettingsService implements ISettingsService {
        private _user: IUser = {
            account: {
                name:               null,
                surname:            null,
                full_name:          null,
                avatar:             null,
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
            'Upload'
        ];


        constructor(
            private $http:angular.IHttpService,
            private Upload: any) {
            // ---------------------------------------------------------------------------------------------------------
        }



        public load(success_callback?, error_callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/account/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.update(response.data['data']['account']);
                        self.update(response.data['data']['preferences']);

                        _.isFunction(success_callback) && success_callback(self._user);
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data);
                });
        }



        public check(field: Object, success_callback?, error_callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/account/', field)
                .then((response) => {
                    if (response.data['code'] === 0) {
                        field['v'] = response.data['value'] ? response.data['value'] : field['v'];

                        var _field = {};
                        _field[field['f']] = field['v'];

                        self.update(_field);
                        _.isFunction(success_callback) && success_callback(field['v']);
                    } else {
                        _.isFunction(error_callback) && error_callback(response.data);
                    }
                }, (response) => {
                    _.isFunction(error_callback) && error_callback(response.data);
                })
        }



        public uploadAvatar(avatar: File, success_callback?, error_callback?) {
            var self = this;

            this.Upload.upload({
                url: '/ajax/api/cabinet/account/photo/',
                file: avatar
            }).success((response) => {
                if (response.code === 0) {
                    self.update({ avatar: response.data['url'] });
                    _.isFunction(success_callback) && success_callback(response);
                } else {
                    _.isFunction(error_callback) && error_callback(response)
                }
            }).error((response) => {
                _.isFunction(error_callback) && error_callback(response)
            })
        }



        public update(params: Object) {
            for (var key in params) {
                if (this._user.account[key] !== undefined) {
                    this._user.account[key] = params[key];

                    if (key === 'name' || key === 'surname') {
                        this._user.account.full_name = this._user.account.name + ' ' + this._user.account.surname;
                    }
                }

                if (this._user.preferences[key] != undefined) {
                    this._user.preferences[key] = params[key];
                }
            }

            this.saveToStorages(this._user);
        }



        public get user() {
            return this._user;
        }



        public clearDataByUser() {
            if (localStorage && localStorage['user']) {
                delete localStorage['user']
            }
        }



        private saveToStorages(user: Object) {
            if (localStorage) {
                localStorage['user'] = JSON.stringify(user);
            }
        }
    }
}