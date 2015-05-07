/// <reference path='_references.ts' />


module bModules.Panels {
    'use strict';

    export class SlidingPanelsHandler implements ISlidingPanelsHandler {
        private panels: SlidingPanel[] = [];

        private close_state_sid:    number = 0;
        private open_state_sid:     number = 1;


        public static $inject = [
            '$rootScope',
            '$state'
        ];

        constructor(private $rootScope: angular.IRootScopeService, private $state: angular.ui.IStateService) {
            this.panels.push(new SlidingPanel(angular.element('.filters-panel'), 'filters'));
            this.panels.push(new SlidingPanel(angular.element('.favorites-panel'), 'favorites'));
            this.panels.push(new SlidingPanel(angular.element('.auth-panel'), 'auth'));

            this.$rootScope.$on('$stateChangeSuccess', () => this.synchronize());
        }



        private synchronize() {
            // Приоритет панелей якщо в урлі для декількох панелей задано значення відкритої
            // -
            if (parseInt(this.$state.params['filters']) !== this.close_state_sid &&
                parseInt(this.$state.params['favorites']) !== this.close_state_sid) {
                // -
                this.$state.go('base', { favorites: this.close_state_sid });
                return;
            }
            if (parseInt(this.$state.params['filters']) !== this.close_state_sid &&
                parseInt(this.$state.params['auth']) !== this.close_state_sid) {
                // -
                this.$state.go('base', { auth: this.close_state_sid });
                return;
            }
            if (parseInt(this.$state.params['favorites']) !== this.close_state_sid &&
                parseInt(this.$state.params['auth']) !== this.close_state_sid) {
                // -
                this.$state.go('base', { auth: this.close_state_sid });
                return;
            }


            this.switchState('filters', parseInt(this.$state.params['filters']));
            this.switchState('favorites', parseInt(this.$state.params['favorites']));
            this.switchState('auth', parseInt(this.$state.params['auth']));
        }



        private switchState(panel_name: string, state: number) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i].panel_name) {
                    panels[i].state = state;

                    this.$rootScope.$broadcast('_modules.Panels.SlidingPanels.PanelSwitchState', {
                        panel_name: panel_name,
                        state: state,
                        is_opened: state !== this.close_state_sid
                    });
                }
            }
        }



        public isOpened(panel_name: string) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i].panel_name)
                    return panels[i].state !== this.close_state_sid
            }
        }



        public open(panel_name: string, state: number = this.open_state_sid) {
            switch (panel_name) {
                case 'filters':
                    this.$state.go('base', { filters: state, favorites: this.close_state_sid, auth: this.close_state_sid });
                    break;
                case 'favorites':
                    this.$state.go('base', { filters: this.close_state_sid, favorites: state, auth: this.close_state_sid });
                    break;
                case 'auth':
                    this.$state.go('base', { filters: this.close_state_sid, favorites: this.close_state_sid, auth: state });
                    break;
            }

            this.$rootScope.$broadcast('_modules.Panels.SlidingPanels.PanelOpened', {
                panel_name: panel_name,
                state: state,
                is_opened: state !== this.close_state_sid
            });
        }



        public close(panel_name: string) {
            switch (panel_name) {
                case 'filters':
                    this.$state.go('base', { filters: this.close_state_sid });
                    break;
                case 'favorites':
                    this.$state.go('base', { favorites: this.close_state_sid });
                    break;
                case 'auth':
                    this.$state.go('base', { auth: this.close_state_sid });
                    break;
            }

            this.$rootScope.$broadcast('_modules.Panels.SlidingPanels.PanelClosed', {
                panel_name: panel_name,
                state: this.close_state_sid,
                is_opened: false
            });
        }
    }
}