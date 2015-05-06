/// <reference path='_references.ts' />


module modules.Panels {
    'use strict';

    export class DropPanelsHandler implements IDropPanelsHandler {
        private panels: DropPanel[] = [];

        private close_state_sid:    number = 0;
        private open_state_sid:     number = 1;


        public static $inject = [
            '$rootScope',
            '$state'
        ];

        constructor(private $rootScope: angular.IRootScopeService, private $state: angular.ui.IStateService) {
            this.panels.push(new DropPanel(angular.element('.user-panel'), 'user'));
            this.panels.push(new DropPanel(angular.element('.menu-panel'), 'menu'));
        }



        public isOpened(panel_name: string) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i].panel_name)
                    return panels[i].state !== this.close_state_sid
            }
        }



        public open(panel_name: string, state: number = this.open_state_sid) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i].panel_name) {
                    panels[i].state = state;

                    this.$rootScope.$broadcast('_modules.Panels.DropPanels.PanelOpened', {
                        panel_name: panel_name,
                        state: state,
                        is_opened: state !== this.close_state_sid
                    });
                }
            }
        }



        public close(panel_name: string) {
            var panels = this.panels;

            for (var i = 0, len = panels.length; i < len; i++) {
                if (panel_name === panels[i].panel_name) {
                    panels[i].state = this.close_state_sid;

                    this.$rootScope.$broadcast('_modules.Panels.DropPanels.PanelClosed', {
                        panel_name: panel_name,
                        state: this.close_state_sid,
                        is_opened: false
                    });
                }
            }
        }
    }
}