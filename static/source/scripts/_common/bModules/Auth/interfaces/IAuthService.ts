/// <reference path='../_references.ts' />


module bModules.Auth {
    export interface IAuthService {
        user: IUser

        login(phoneNumber: string, success?: Function, error?: Function): void

        tryLogin(success?: Function, error?: Function): void

        loadProfile(success?: Function, error?: Function): void

        checkProfileField(field: Object, success?: Function, error?: Function): void

        uploadAvatar(avatar: File, success?: Function, error?: Function): void
    }
}