namespace Mappino.Core.BAuth {

    import IHttpService     = angular.IHttpService;
    import IHttpPromise     = angular.IHttpPromise;
    import ICookiesService  = angular.cookies.ICookiesService;
    import IUploadService   = angular.angularFileUpload.IUploadService;
    import IUploadPromise   = angular.angularFileUpload.IUploadPromise;

    'use strict';


    export class BAuthService {
        private _user: User;

        public static $inject = [
            '$http',
            '$cookies',
            'Upload'
        ];


        constructor(private $http: IHttpService,
                    private $cookies: ICookiesService,
                    private Upload: IUploadService) {
            // ---------------------------------------------------------------------------------------------------------
            this._user = new User();
        }



        public checkPhoneNumber(phoneCode: string, phonePhone: string): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/login/`, {
                'mobile_code':   phoneCode,
                'mobile_phone':  phonePhone
            });

            promise.success(response => { /* success */ });

            promise.error(response => { /* error */ });

            return promise;
        }



        public checkSMSCode(mobileCode: string, mobilePhone: string, token: string): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/login/check-code/`, {
                'mobile_code':  mobileCode,
                'mobile_phone': mobilePhone,
                'token':        token
            });

            promise.success(response => {
                var userData = response.data;

                for (var key in userData) {
                    if (userData.hasOwnProperty(key))
                        this._user.set(key, userData[key]);
                }

                this.$cookies.remove('mcheck');
            });

            promise.error(response => { /* error */ });

            return promise;
        }




        public tryLogin(): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.get(`/ajax/api/accounts/on-login-info/`);

            promise.success(response => {
                var userData = response.data;

                for (var key in userData) {
                    if (userData.hasOwnProperty(key))
                        this._user.set(key, userData[key]);
                }
            });

            promise.error(response => {
                this.$cookies.remove('user');
                this.$cookies.remove('sessionid');
            });

            return promise;
        }



        public loadProfile(): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/account/`);

            promise.success(response => {
                var userData            = response.data;
                var userDataAccount     = userData.account;
                var userDataPreferences = userData.preferences;

                for (var key in userDataAccount) {
                    if (userDataAccount.hasOwnProperty(key))
                        this._user.set(key, userDataAccount[key]);
                }

                for (var key in userDataPreferences) {
                    if (userDataPreferences.hasOwnProperty(key))
                        this._user.set(key, userDataPreferences[key]);
                }
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public updateProfileField(fieldName: string, fieldValue: number|string, fieldValuePrefix?: number|string): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/account/`, {
                [fieldName]: `${fieldValuePrefix ? fieldValuePrefix : ''}${fieldValue}`
            });

            promise.success(response => {
                if (response.code == 0) {
                    this._user.set(fieldName, fieldValue);
                }
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public uploadAvatar(avatar: File): IUploadPromise<any> {
            var promise: IUploadPromise<any> = this.Upload.upload({
                url: `/ajax/api/cabinet/account/photo/`,
                method: 'POST',
                file: avatar
            });

            promise.success(response => {
                this._user.set('avatar_url', response.data.url);
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public removeAvatar(): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/account/photo/`);

            promise.success(response => {
                this._user.set('avatar_url', undefined);
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public logout(): IHttpPromise<any> {
            var promise: IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/logout/`, null);

            promise.success(response => {
                this.$cookies.remove('user');
                this.$cookies.remove('sessionid');
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public get user() {
            return this._user.get();
        }
    }
}