/// <reference path='../_references.ts' />


module bModules.Auth {
    export interface IAuthService {
        login(username: string, password: string, success?: Function, error?: Function): void

        tryLogin(success?: Function, error?: Function): void
    }
}