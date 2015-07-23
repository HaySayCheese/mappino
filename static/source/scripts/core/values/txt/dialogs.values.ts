

module Mappino.Core.Values {
    export class DialogsValues {
        static get Default(): any {
            return {
                'REMOVE_PUBLICATION': {
                    TITLE:      'Подтвердите удаление объявления',
                    BODY:       'Вы уверенны, что хотите удалить объявление?',
                    ARIA_LABEL: 'Вы уверенны, что хотите удалить объявление?',
                    OK_BTN:     'Да, удалить',
                    CANCEL_BTN: 'Отмена'
                },


                'RECOVERY_PUBLICATION': {
                    TITLE:      'RECOVERY_PUBLICATION_TITLE',
                    BODY:       'RECOVERY_PUBLICATION_BODY',
                    ARIA_LABEL: 'RECOVERY_PUBLICATION_BODY',
                    OK_BTN:     'RECOVERY_PUBLICATION_OK_BTN',
                    CANCEL_BTN: 'RECOVERY_PUBLICATION_CANCEL_BTN'
                },


                'DONE_EDITING_LATER_PUBLICATION': {
                    TITLE:      'Сохранение объявления',
                    BODY:       'Объявление успешно сохранено',
                    ARIA_LABEL: 'Объявление успешно сохранено',
                    OK_BTN:     'Хорошо'
                },


                'EDIT_PUBLICATION': {
                    TITLE:      'Редактирование объявления',
                    BODY:       'Выбранное объявление опубликовано, для продолжения редактирования его следуют снять с публикации. Вы уверенны, что хотите продолжить?',
                    ARIA_LABEL: 'Выбранное объявление опубликовано, для продолжения редактирования его следуют снять с публикации. Вы уверенны, что хотите продолжить?',
                    OK_BTN:     'Да, продолжить',
                    CANCEL_BTN: 'Отмена'
                },


                'ALL_MEANS_OF_COMMUNICATION_DISABLED': {
                    TITLE:      'Вы - человек-невидимка?',
                    BODY:       'Вы только что отключили все способы связи с Вами. Возможно, стоит пересмотреть настройки.',
                    ARIA_LABEL: 'Вы только что отключили все способы связи с Вами. Возможно, стоит пересмотреть настройки.',
                    OK_BTN:     'Да, спасибо'
                }
            };
        }
    }
}