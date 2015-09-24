

namespace Mappino.Core.Constants {
    export class RealtyTypes {
        static get Default(): any {
            return [
                {
                    id:             0,
                    name:           "flat",
                    titles: {
                        singular:   "Квартира",
                        plural:     "Квартиры",
                        genitive:   "Квартиры"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_c_min", "p_c_max",
                        "r_d_min", "r_d_max",
                        "p_min", "p_max", "cu_sid",
                        "r_c_min", "r_c_max",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             1,
                    name:           "house",
                    titles: {
                        singular:   "Дом",
                        plural:     "Дома",
                        genitive:   "Дома"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_c_min", "p_c_max",
                        "r_d_min", "r_d_max",
                        "p_min", "p_max", "cu_sid",
                        "r_c_min", "r_c_max",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             2,
                    name:           "room",
                    titles: {
                        singular:   "Комната",
                        plural:     "Комнаты",
                        genitive:   "Комнаты"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_c_min", "p_c_max",
                        "r_d_min", "r_d_max",
                        "p_min", "p_max", "cu_sid",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             3,
                    name:           "land",
                    titles: {
                        singular:   "Земельный участок",
                        plural:     "Земельные участки",
                        genitive:   "Земельного участка"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_min", "p_max", "cu_sid",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             4,
                    name:           "garage",
                    titles: {
                        singular:   "Гараж",
                        plural:     "Гаражи",
                        genitive:   "Гаража"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_min", "p_max", "cu_sid",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             5,
                    name:           "office",
                    titles: {
                        singular:   "Офис",
                        plural:     "Офисы",
                        genitive:   "Офиса"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "r_d_min", "r_d_max",
                        "p_min", "p_max", "cu_sid",
                        "c_c_min", "c_c_max",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             6,
                    name:           "trade",
                    titles: {
                        singular:   "Торговое помещение",
                        plural:     "Торговые помещения",
                        genitive:   "Торгового помещения"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "r_d_min", "r_d_max",
                        "p_min", "p_max", "cu_sid",
                        "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             7,
                    name:           "warehouse",
                    titles: {
                        singular:   "Склад",
                        plural:     "Склады",
                        genitive:   "Склада"
                    },
                    filters: [
                        "op_sid", "pr_sid",
                        "p_min", "p_max", "cu_sid",
                        "t_a_min", "t_a_max"
                    ]
                }
            ];
        }
    }
}