
// todo: перекласти назви на англ мову
module Mappino.Core.Values {
    export class DialogsValues {
        static get Default(): any {
            return {
                'REMOVE_PUBLICATION': {
                    TITLE:      'REMOVE_PUBLICATION_TITLE',
                    BODY:       'REMOVE_PUBLICATION_BODY',
                    ARIA_LABEL: 'REMOVE_PUBLICATION_BODY',
                    OK_BTN:     'REMOVE_PUBLICATION_OK_BTN',
                    CANCEL_BTN: 'REMOVE_PUBLICATION_CANCEL_BTN'
                },

                'DONE_EDITING_LATER_PUBLICATION': {
                    TITLE:      'DONE_EDITING_LATER_PUBLICATION_TITLE',
                    BODY:       'DONE_EDITING_LATER_PUBLICATION_BODY',
                    ARIA_LABEL:  'DONE_EDITING_LATER_PUBLICATION_LABEL',
                    OK_BTN:     'DONE_EDITING_LATER_PUBLICATION_OK_BTN'
                }
            };
        }
    }
}