/// <reference path='../_references.ts' />


module bModules.Auth {
    export interface ISettingsService {
        user: IUser

        load(success_callback?, error_callback?): void

        /**
         * @param field.f - name of input field
         * @param field.v - value of input field
         */
        check(field: Object, success_callback?, error_callback?): void

        uploadAvatar(avatar: File, success_callback?, error_callback?): void

        update(params: Object): void

        clearDataByUser(): void
    }
}