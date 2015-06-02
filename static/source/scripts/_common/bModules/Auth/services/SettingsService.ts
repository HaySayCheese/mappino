/// <reference path='../_references.ts' />


module bModules.Auth {

    export class SettingsService {
        private _user: Object = {
            account: {
                name:               '',
                surname:            '',
                full_name:          '',
                avatar:             '',
                add_landline_phone: '',
                add_mobile_phone:   '',
                email:              '',
                landline_phone:     '',
                mobile_phone:       '',
                skype:              '',
                work_email:         '',
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
            // -
        }



        public load(callback?) {
            var self = this;

            this.$http.get('/ajax/api/cabinet/account/')
                .then((response) => {
                    if (response.data['code'] === 0) {
                        self.update(response.data['data']['account']);
                        self.update(response.data['data']['preferences']);

                        _.isFunction(callback) && callback(self._user);
                    } else {
                        _.isFunction(callback) && callback(response);
                    }
                }, () => {
                    // - error
                });
        }



        public check(field: Object, callback?) {
            var self = this;

            this.$http.post('/ajax/api/cabinet/account/', field)
                .then((response) => {
                    field['v'] = response.data['value'] ? response.data['value'] : field['v'];

                    var _field = {};
                    _field[field['f']] = field['v'];

                    self.update(_field);
                    _.isFunction(callback) && callback(field['v'], response.data['code']);
                })
        }



        public uploadAvatar(avatar: File, callback?) {
            var self = this;

            this.Upload.upload({
                url: '/ajax/api/cabinet/account/photo/',
                file: avatar
            }).success((response) => {
                if (response.code === 0) {
                    self.update({ avatar: response.data['url'] });
                    _.isFunction(callback) && callback(response);
                } else {
                    _.isFunction(callback) && callback(response)
                }
            })
        }



        public update(user: Object) {
            for (var key in user) {
                if (this._user['account'][key] !== undefined) {
                    this._user['account'][key] = user[key];

                    if (key === 'name' || key === 'surname') {
                        this._user['account']['full_name'] = this._user['account']['name'] + ' ' + this._user['account']['surname'];
                    }
                }

                if (this._user['preferences'][key] != undefined) {
                    this._user['preferences'][key] = user[key];
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