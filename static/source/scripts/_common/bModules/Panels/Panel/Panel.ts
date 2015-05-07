
module bModules.Panels {

    export class Panel {
        config: Object = {
            openedClass:    'opened',
            closedClass:    'closed',
            closingClass:   'closing'
        };

        constructor(public _el: JQuery, public _panel_name: string, public _state: number = 0) {
            // -
        }



        get panel_name() {
            return this._panel_name;
        }



        get state() {
            return this._state;
        }

        set state(state: number) {
            if (this._state !== state) {
                this._state = state;
                state === 0 ? this.hide() : this.show();
            }
        }



        private show() {
            this._el
                .dequeue()
                .removeClass(this.config['closedClass'])
                .removeClass(this.config['closingClass'])
                .addClass(this.config['openedClass']);
        }



        private hide() {
            var self = this;
            // Якщо панель має клас 'this.config['openedClass']' (відкрита)
            // то закриваємо її
            // ця провірка потрібна що б не смикати панель спочатку у відкритий стан а потім закривати
            if (this._el.hasClass(this.config['openedClass'])) {

                this._el
                    .removeClass(this.config['openedClass'])
                    .addClass(this.config['closingClass'])
                    .delay(500)
                    .queue(function () {
                        self._el
                            .removeClass(self.config['closingClass'])
                            .addClass(self.config['closedClass'])
                            .dequeue();
                    })
            } else {
                this._el.addClass(this.config['closedClass'])
            }
        }
    }
}