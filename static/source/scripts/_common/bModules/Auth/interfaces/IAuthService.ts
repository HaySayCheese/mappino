/// <reference path='../_references.ts' />


module bModules.Auth {
    export interface IAuthService {
        login(user: IUser, success_callback?, error_callback?): void

        getUserByCookie(success_callback?, error_callback?): void
    }
}