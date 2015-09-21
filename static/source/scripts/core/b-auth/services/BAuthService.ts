namespace Mappino.Core.BAuth {

    export class BAuthService {
        private _user: User;

        public static $inject = [
            '$http',
            '$cookies',
            'Upload'
        ];


        constructor(private $http: ng.IHttpService,
                    private $cookies: ng.cookies.ICookiesService,
                    private Upload: any) {
            // ---------------------------------------------------------------------------------------------------------
            this._user = new User();
        }



        public checkPhoneNumber(phoneCode: string, phonePhone: string): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/login/`, {
                'mobile_code':   phoneCode,
                'mobile_phone':  phonePhone
            });

            promise.success(response => { /* success */ });

            promise.error(response => { /* error */ });

            return promise;
        }



        public checkSMSCode(phoneCode: string, phonePhone: string, smsCode: string): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/login/check-code/`, {
                'mobile_code':  phoneCode,
                'mobile_phone': phonePhone,
                'token':        smsCode
            });

            promise.success(response => {
                this._user.set(response.data);
                this.$cookies.remove('mcheck');
            });

            promise.error(response => { /* error */ });

            return promise;
        }




        public tryLogin(): ng.IHttpPromise<any> {
            //if (!this.$cookies.get('user')) return;

            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/accounts/on-login-info/`);

            promise.success(response => {
                this._user.set(response.data);
            });

            promise.error(response => {
                this.$cookies.remove('user');
                this.$cookies.remove('sessionid');
            });

            return promise;
        }



        public loadProfile(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.get(`/ajax/api/cabinet/account/`);

            promise.success(response => {
                this._user.set(response.data.account);
                this._user.set(response.data.preferences);
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public checkProfileField(field): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/cabinet/account/`, field);

            promise.success(response => {
                this._user.set(field);
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public uploadAvatar(avatar: File): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.Upload.upload({
                url: `/ajax/api/cabinet/account/photo/`,
                file: avatar
            });

            promise.success(response => {
                this._user.set({ avatar_url: response.data.url });
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public removeAvatar(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.delete(`/ajax/api/cabinet/account/photo/`);

            promise.success(response => {
                this._user.set({ avatar_url: null });
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public logout(): ng.IHttpPromise<any> {
            var promise: ng.IHttpPromise<any> = this.$http.post(`/ajax/api/accounts/logout/`, null);

            promise.success(response => {
                this.$cookies.remove('user');
            });

            promise.error(response => { /* error */ });

            return promise;
        }



        public get user() {
            return this._user.get();
        }
    }
}