/// <reference path='_references.ts' />


module modules.Panels {

    export class DropPanel extends Panel {
        constructor(public _el: JQuery, public _panel_name: string, public _state: number = 0) {
            super(_el, _panel_name, _state);
        }
    }
}