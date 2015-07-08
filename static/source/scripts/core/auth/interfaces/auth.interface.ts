module mappino.core.auth {
    export interface IAuthService {
        user: IUser

        checkPhoneNumber(phoneNumber: string, success?: Function, error?: Function): void

        checkSMSCode(phoneNumber: string, smsCode: string, success?: Function, error?: Function): void

        tryLogin(success?: Function, error?: Function): void

        loadProfile(success?: Function, error?: Function): void

        checkProfileField(field: Object, success?: Function, error?: Function): void

        uploadAvatar(avatar: File, success?: Function, error?: Function): void
    }
}