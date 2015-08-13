module Mappino.Core.BAuth {
    export interface IUser {
        account: {
            first_name:         string
            last_name:          string
            full_name:          string
            avatar_url:         string
            mobile_code:        string
            mobile_phone:       string
            add_mobile_code:    string
            add_mobile_phone:   string
            landline_phone:     string
            add_landline_phone: string
            email:              string
            skype:              string
            work_email:         string
        }

        preferences: {
            allow_call_requests:            boolean
            allow_messaging:                boolean
            hide_add_landline_phone_number: boolean
            hide_add_mobile_phone_number:   boolean
            hide_email:                     boolean
            hide_landline_phone_number:     boolean
            hide_mobile_phone_number:       boolean
            hide_skype:                     boolean

            send_call_request_notifications_to_sid: number
            send_message_notifications_to_sid:      number
        }
    }
}