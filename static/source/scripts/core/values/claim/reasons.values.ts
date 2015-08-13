
// todo: перекласти назви на англ мову
namespace Mappino.Core.Values {
    export class ClaimReasonsValues {
        static get Default(): any {
            return [{
                id:     0,
                name:   'other',
                title:  'Другое'
            }, {
                id:     1,
                name:   'owner_is_and_intermediary',
                title:  'Владелец объявления - посредник'
            }, {
                id:     2,
                name:   'untruthful_content',
                title:  'Объявление содержит подозрительный контент'
            }, {
                id:     3,
                name:   'photos_do_not_correspond_to_reality',
                title:  'Фото не соответствуют реальности'
            }];
        }
    }
}