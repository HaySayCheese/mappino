module Mappino.Core.BAuth {
    export interface IAuthService {
        user: IUser

        checkPhoneNumber(phoneNumber: string, successCallback?: Function, errorCallback?: Function): void

        checkSMSCode(phoneNumber: string, smsCode: string, successCallback?: Function, errorCallback?: Function): void

        tryLogin(successCallback?: Function, errorCallback?: Function): void

        loadProfile(successCallback?: Function, errorCallback?: Function): void

        checkProfileField(field: Object, successCallback?: Function, errorCallback?: Function): void

        uploadAvatar(avatar: File, successCallback?: Function, errorCallback?: Function): void

        removeAvatar(successCallback?: Function, errorCallback?: Function): void

        logout(successCallback?: Function, errorCallback?: Function): void
    }
}