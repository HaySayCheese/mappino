/// <reference path='../_references.ts' />


module mappino.main.map {
    'use strict';

    export class PanelsHandler implements IPanelsHandler {
        private panels: Panel[] = [];

        private closedStateId: number = 0;


        public static $inject = [
            '$rootScope',
            '$state'
        ];

        constructor(private $rootScope: angular.IRootScopeService, private $state: angular.ui.IStateService) {
            this.panels.push(new Panel(angular.element('.filters-panel'), 'filters', 0));
            this.panels.push(new Panel(angular.element('.favorites-panel'), 'favorites', 0));

            this.$rootScope.$on('$stateChangeSuccess', () => this.synchronize());
        }



        private synchronize() {
            // Якщо в урлі для панелі фільтрів та оголошення параметри стану !== 0
            // значить хочуть бути відкрти обидві панелі і у нас конфлікт.
            // Тоді закриваємо панель фільтрів, віддаючи приоритет панелі з оголошенням
            if (parseInt(this.$state.params['filters']) !== this.closedStateId &&
                parseInt(this.$state.params['favorites']) !== this.closedStateId) {
                // -
                this.$state.go('base', { favorites: 0 });
                return;
            }

            this.toggleState('filters', parseInt(this.$state.params['filters']));
            this.toggleState('favorites', parseInt(this.$state.params['favorites']));
        }



        private toggleState(panel_name: string, state: number) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i]._name) {
                    panels[i]._state = state;
                }
            }
        }



        public isOpened(panel_name: string) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i]._name)
                    return panels[i]._state !== this.closedStateId
            }
        }



        public open(panel_name: string) {
            var self = this;

            switch (panel_name) {
                case 'filters':
                    self.$state.go('base', { favorites: self.closedStateId, filters: 1 });
                    break;
                case 'favorites':
                    self.$state.go('base', { filters: self.closedStateId, favorites: 1 });
                    break;
            }
        }



        public close(panel_name: string) {
            var self = this;

            switch (panel_name) {
                case 'filters':
                    self.$state.go('base', { filters: self.closedStateId });
                    break;
                case 'favorites':
                    self.$state.go('base', { favorites: self.closedStateId });
                    break;
            }
        }
    }
}