
// todo: перекласти назви на англ мову
namespace Mappino.Core.Values {
    export class BuildingTypesValues {
        static get Default(): any {
            return [{
                id:     '0',
                name:   'other',
                title:  'Другой'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'Панель'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'Кирпич'
            }, {
                id:     '3',
                name:   'not_defined',
                title:  'Хрущевка'
            }, {
                id:     '4',
                name:   'not_defined',
                title:  'Монолит'
            }, {
                id:     '5',
                name:   'not_defined',
                title:  'Дореволюционний'
            }, {
                id:     '6',
                name:   'not_defined',
                title:  'Малосемейка'
            }, {
                id:     '7',
                name:   'not_defined',
                title:  'Индивидуальный проект'
            }, {
                id:     '8',
                name:   'not_defined',
                title:  'Неизвестно'
            }];
        }


        static get Trade(): any {
            return [{
                id:     '0',
                name:   'not_defined',
                title:  'В жилом здании'
            }, {
                id:     '1',
                name:   'not_defined',
                title:  'В торгово-развлекательном центре'
            }, {
                id:     '2',
                name:   'not_defined',
                title:  'В бизнес-центре'
            }, {
                id:     '3',
                name:   'not_defined',
                title:  'В административном здании'
            }, {
                id:     '4',
                name:   'not_defined',
                title:  'В отдельном здании'
            }];
        }
    }
}