/// <reference path='../_references.ts' />


module mappino.main.map {
    export class Panel {
        config: Object = {
            openedClass:    'opened',
            closedClass:    'closed',
            closingClass:   'closing'
        };

        constructor(private el: JQuery, private name: string, private state: number) {
            // -
        }



        get _name() {
            return this.name;
        }



        get _state() {
            return this.state;
        }

        set _state(_state: number) {
            this.state = _state;
            _state === 0 ? this.hide() : this.show();
        }



        private show() {
            this.el
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
            if (this.el.hasClass(this.config['openedClass'])) {

                this.el
                    .removeClass(this.config['openedClass'])
                    .addClass(this.config['closingClass'])
                    .delay(500)
                    .queue(function () {
                        self.el
                            .removeClass(self.config['closingClass'])
                            .addClass(self.config['closedClass'])
                            .dequeue();
                    })
            } else {
                this.el.addClass(this.config['closedClass'])
            }
        }
    }
}