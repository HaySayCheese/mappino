/// <reference path='../_references.ts' />


module pages.home {
    export class HomeController {

        public static $inject = [
            '$scope',
            '$timeout'
        ];

        constructor(
            private $scope: angular.IScope,
            private $timeout: angular.ITimeoutService) {
            // -
            $timeout(() => $('.parallax').parallax());


            this.setParalaxHeight();
        }


        private setParalaxHeight() {
            $(window).on('resize', function() {
                if ($(window).height() > 300) {
                    $('.parallax-container:first-child').css('height', $(window).height() + 'px');
                }
            }).resize();
        }


        private static scrollTo(to: string) {
            $("html, body").animate({
                scrollTop: to === 'top' ? 0 : $(window).height()
            }, '500');

            event.preventDefault();
        }
    }
}