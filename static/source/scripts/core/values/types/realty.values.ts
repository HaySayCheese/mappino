

module Mappino.Core.Values {
    export class RealtyTypesValues {
        static get Default(): any {
            return [
                {
                    id:             0,
                    name:           "flat",
                    titles: {
                        singular:   "Квартира",
                        plural:     "Квартиры",
                        nominative: "Квартиры"
                    },
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                        "msd", "grd", "pl_sid", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                    ]
                }, {
                    id:             1,
                    name:           "house",
                    titles: {
                        singular:   "Дом",
                        plural:     "Дома",
                        nominative: "Дома"
                    },
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "f_c_min", "f_c_max", "elt", "h_w",
                        "gas", "c_w", "swg", "h_t_sid"
                    ]
                }, {
                    id:             2,
                    name:           "room",
                    titles: {
                        singular:   "Комната",
                        plural:     "Комнаты",
                        nominative: "Комнаты"
                    },
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                        "msd", "grd", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                    ]
                }, {
                    id:             3,
                    name:           "land",
                    titles: {
                        singular:   "Земельный участок",
                        plural:     "Земельные участки",
                        nominative: "Земельного участка"
                    },
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "a_min", "a_max", "gas", "elt", "wtr", "swg"
                    ]
                }, {
                    id:             4,
                    name:           "garage",
                    titles: {
                        singular:   "Гараж",
                        plural:     "Гаражи",
                        nominative: "Гаража"
                    },
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "t_a_min", "t_a_max"
                    ]
                }, {
                    id:             5,
                    name:           "office",
                    titles: {
                        singular:   "Офис",
                        plural:     "Офисы",
                        nominative: "Офиса"
                    },
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "t_a_min", "t_a_max",
                        "c_c_min", "c_c_max", "sct", "ktn", "h_w", "c_w"
                    ]
                }, {
                    id:             6,
                    name:           "trade",
                    titles: {
                        singular:   "Торговое помещение",
                        plural:     "Торговые помещения",
                        nominative: "Торгового помещения"
                    },
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                        "t_a_min", "t_a_max", "b_t_sid", "gas", "elt", "h_w", "c_w", "swg"
                    ]
                }, {
                    id:             7,
                    name:           "warehouse",
                    titles: {
                        singular:   "Склад",
                        plural:     "Склады",
                        nominative: "Склада"
                    },
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                        "gas", "elt", "h_w", "c_w", "s_a", "f_a"
                    ]
                }
            ];
        }
    }
}