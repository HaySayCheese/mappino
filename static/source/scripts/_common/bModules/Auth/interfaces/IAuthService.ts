/// <reference path='../_references.ts' />


module bModules.Auth {
    export interface IAuthService {
        login(user: IUserToLogin, success?: Function, error?: Function): void

        tryLogin(success?: Function, error?: Function): void

        registration(user: IUserToRegistration, success?: Function, error?: Function): void

        validateEmail(email: string, success?: Function, error?: Function): void

        validatePhoneNumber(phoneNumber: string, success?: Function, error?: Function): void

    }
}