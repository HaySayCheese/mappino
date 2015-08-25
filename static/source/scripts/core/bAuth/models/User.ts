namespace Mappino.Core.BAuth {
    export class User {

        private account: any = {
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
        };

        private preferences: any = {
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
        };

        constructor() {}



        public set(params: any) { // todo: fix this to Object type
            for (var key in params) {
                if (params.hasOwnProperty(key)) {
                    if (angular.isDefined(this.account[key])) {
                        this.account[key] = params[key];

                        if (key === 'first_name' || key === 'last_name') {
                            if (this.account.first_name != null && this.account.last_name != null) {
                                this.account.full_name = this.account.first_name + ' ' + this.account.last_name;
                            }
                        }
                    }

                    if (angular.isDefined(this.preferences[key])) {
                        this.preferences[key] = params[key];
                    }
                }
            }
        }


        public get() {
            return {
                account:        this.account,
                preferences:    this.preferences
            }
        }
    }
}