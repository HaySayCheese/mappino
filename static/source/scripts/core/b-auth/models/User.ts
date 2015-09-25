namespace Mappino.Core.BAuth {
    export class User {

        private _fields: any = {
            // account
            first_name:             undefined,
            last_name:              undefined,
            full_name:              undefined,

            mobile_code:            undefined,
            mobile_phone:           undefined,
            full_mobile_phone:      undefined,

            add_mobile_code:        undefined,
            add_mobile_phone:       undefined,
            full_add_mobile_phone:  undefined,

            landline_phone:         undefined,
            add_landline_phone:     undefined,

            email:                  undefined,
            work_email:             undefined,

            skype:                  undefined,

            avatar_url:             undefined,


            // preferences
            allow_call_requests:            undefined,
            allow_messaging:                undefined,

            hide_add_landline_phone_number: undefined,
            hide_add_mobile_phone_number:   undefined,
            hide_email:                     undefined,
            hide_landline_phone_number:     undefined,
            hide_mobile_phone_number:       undefined,
            hide_skype:                     undefined,

            send_call_request_notifications_to_sid: undefined, //0,
            send_message_notifications_to_sid:      undefined //0
        };


        constructor() {}



        public set(key: string, value: any) {
            if (this._fields.hasOwnProperty(key)) {
                this._fields[key] = value;
            }

            switch (key) {
                case 'first_name':
                    this.createFullName();
                    break;
                case 'last_name':
                    this.createFullName();
                    break;

                case 'mobile_code':
                    this.createFullMobilePhone();
                    break;
                case 'mobile_phone':
                    this.createFullMobilePhone();
                    break;

                case 'add_mobile_code':
                    this.createFullAddMobilePhone();
                    break;
                case 'add_mobile_phone':
                    this.createFullAddMobilePhone();
                    break;
            }
        }



        public get() {
            return this._fields;
        }



        private createFullName() {
            this._fields.full_name =
                `${this._fields.first_name ? this._fields.first_name : ''} ${this._fields.last_name ? this._fields.last_name: ''}`;
        }



        private createFullMobilePhone() {
            if (this._fields.mobile_code && this._fields.mobile_phone)
                this._fields.full_mobile_phone = `${this._fields.mobile_code}${this._fields.mobile_phone}`;
        }



        private createFullAddMobilePhone() {
            if (this._fields.add_mobile_code && this._fields.add_mobile_phone)
                this._fields.full_add_mobile_phone = `${this._fields.add_mobile_code}${this._fields.add_mobile_phone}`;
        }
    }
}