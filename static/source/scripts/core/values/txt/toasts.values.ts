
// todo: перекласти назви на англ мову
module Mappino.Core.Values {
    export class ToastsValues {
        static get Default(): any {
            return {
                'PUBLICATION': {
                    'CREATE': {
                        'TITLE': 'CREATE_PUBLICATION_TITLE'
                    },

                    'REMOVE': {
                        'TITLE': 'REMOVE_PUBLICATION_TITLE'
                    },

                    'PUBLISH': {
                        'TITLE': 'PUBLISH_PUBLICATION_TITLE'
                    },

                    'LOAD': {
                        'TITLE': 'LOAD_PUBLICATION_TITLE'
                    },

                    'UPLOAD_PHOTO': {
                        'TITLE': 'UPLOAD_PUBLICATION_PHOTO_TITLE'
                    },

                    'REMOVE_PHOTO': {
                        'TITLE': 'REMOVE_PUBLICATION_PHOTO_TITLE'
                    },

                    'SET_TITLE_PHOTO': {
                        'TITLE': 'SET_PUBLICATION_TITLE_PHOTO_TITLE'
                    },

                    'CHECK_FIELD': {
                        'TITLE': 'CHECK_PUBLICATION_FIELD_TITLE'
                    },

                    'LOAD_BRIEFS': {
                        'TITLE': 'LOAD_PUBLICATIONS_BRIEFS_TITLE'
                    }
                },


                'TICKETS': {
                    'CREATE': {
                        'TITLE': 'CREATE_TICKET_TITLE'
                    },

                    'LOAD': {
                        'TITLE': 'LOAD_TICKETS_TITLE'
                    },

                    'LOAD_TICKET_MESSAGES': {
                        'TITLE': 'LOAD_TICKET_MESSAGES_TITLE'
                    },

                    'SEND_TICKET_MESSAGE': {
                        'TITLE': 'SEND_TICKET_MESSAGE_TITLE'
                    }
                }
            };
        }
    }
}