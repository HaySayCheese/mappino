

module Mappino.Core.Values {
    export class ToastsValues {
        static get Default(): any {
            return {
                'PUBLICATION': {
                    'CREATE': {
                        'TITLE': 'Во время создания объявления возникла ошибка'
                    },

                    'REMOVE': {
                        'TITLE': 'Во время удаления объявления возникла ошибка'
                    },

                    'PUBLISH': {
                        'TITLE': 'Во время публикации объяления возникла ошибка'
                    },

                    'UNPUBLISH': {
                        'TITLE': 'Во время обработки объяления возникла ошибка'
                    },

                    'LOAD': {
                        'TITLE': 'Во время загрузки объяления возникла ошибка'
                    },

                    'UPLOAD_PHOTO': {
                        'TITLE': 'Во время загрузки фото возникла ошибка'
                    },

                    'REMOVE_PHOTO': {
                        'TITLE': 'Во время удаления фото возникла ошибка'
                    },

                    'SET_TITLE_PHOTO': {
                        'TITLE': 'Во время обработки фото возникла ошибка'
                    },

                    'CHECK_FIELD': {
                        'TITLE': 'Во время проверки значения поля возникла ошибка'
                    },

                    'LOAD_BRIEFS': {
                        'TITLE': 'Во время загрузки объявлений возникла ошибка'
                    }
                },


                'TICKETS': {
                    'CREATE': {
                        'TITLE': 'Во время воздания тикета возникла ошибка'
                    },

                    'LOAD': {
                        'TITLE': 'Во время загрузки сообщений возникла ошибка'
                    },

                    'LOAD_TICKET_MESSAGES': {
                        'TITLE': 'Во время загрузки сообщений возникла ошибка'
                    },

                    'SEND_TICKET_MESSAGE': {
                        'TITLE': 'Во время отправки сообщения возникла ошибка'
                    }
                }
            };
        }
    }
}