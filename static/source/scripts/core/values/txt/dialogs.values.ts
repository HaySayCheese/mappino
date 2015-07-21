
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

                'RECOVERY_PUBLICATION': {
                    TITLE:      'RECOVERY_PUBLICATION_TITLE',
                    BODY:       'RECOVERY_PUBLICATION_BODY',
                    ARIA_LABEL: 'RECOVERY_PUBLICATION_BODY',
                    OK_BTN:     'RECOVERY_PUBLICATION_OK_BTN',
                    CANCEL_BTN: 'RECOVERY_PUBLICATION_CANCEL_BTN'
                },

                'DONE_EDITING_LATER_PUBLICATION': {
                    TITLE:      'DONE_EDITING_LATER_PUBLICATION_TITLE',
                    BODY:       'DONE_EDITING_LATER_PUBLICATION_BODY',
                    ARIA_LABEL: 'DONE_EDITING_LATER_PUBLICATION_LABEL',
                    OK_BTN:     'DONE_EDITING_LATER_PUBLICATION_OK_BTN'
                },

                'EDIT_PUBLICATION': {
                    TITLE:      'EDIT_PUBLICATION_TITLE',
                    BODY:       'EDIT_PUBLICATION_BODY',
                    ARIA_LABEL: 'EDIT_PUBLICATION_LABEL',
                    OK_BTN:     'EDIT_PUBLICATION_OK_BTN',
                    CANCEL_BTN: 'EDIT_PUBLICATION_CANCEL_BTN'
                },

                'ALL_MEANS_OF_COMMUNICATION_DISABLED': {
                    TITLE:      'ALL_MEANS_OF_COMMUNICATION_DISABLED_TITLE',
                    BODY:       'ALL_MEANS_OF_COMMUNICATION_DISABLED_BODY',
                    ARIA_LABEL: 'ALL_MEANS_OF_COMMUNICATION_DISABLED_LABEL',
                    OK_BTN:     'ALL_MEANS_OF_COMMUNICATION_DISABLED_OK_BTN'
                }
            };
        }
    }
}