/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class AppController {
        private _location_search: any;

        public static $inject = [
            '$rootScope',
            '$location',
            'DropPanelsHandler',
            'SlidePanelsHandler'
        ];

        constructor(
            private $rootScope,
            private $location,
            private dropPanelsHandler: bModules.Panels.IDropPanelsHandler,
            private slidingPanelsHandler: bModules.Panels.ISlidingPanelsHandler) {
            // -
            var self = this;

            /**
             * Відновлюємо фільтри в урлі після зміни панелі
             **/
            $rootScope.$on('$stateChangeStart', function() {
                if (!_.isNull($location.search()))
                    self._location_search = $location.search();
            });
            $rootScope.$on('$stateChangeSuccess', function() {
                if (!_.isNull(self._location_search))
                    $location.search(self._location_search);
            });
        }
    }
}