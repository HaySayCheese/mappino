

module mappino.core.constants {
    export class RealtyTypesConstant {
        static get Default(): any {
            return [
                {
                    id:     '0',
                    name:   "flat",
                    title:  "Квартиры",
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                        "msd", "grd", "pl_sid", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                    ]
                }, {
                    id:     '1',
                    name:   "house",
                    title:  "Дома",
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "f_c_min", "f_c_max", "elt", "h_w",
                        "gas", "c_w", "swg", "h_t_sid"
                    ]
                }, {
                    id:     '2',
                    name:   "room",
                    title:  "Комнаты",
                    filters: [
                        "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                        "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                        "msd", "grd", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
                    ]
                }, {
                    id:     '3',
                    name:   "land",
                    title:  "Земельные участки",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "a_min", "a_max", "gas", "elt", "wtr", "swg"
                    ]
                }, {
                    id:     '4',
                    name:   "garage",
                    title:  "Гаражи",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "t_a_min", "t_a_max"
                    ]
                }, {
                    id:     '5',
                    name:   "office",
                    title:  "Офисы",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "t_a_min", "t_a_max",
                        "c_c_min", "c_c_max", "sct", "ktn", "h_w", "c_w"
                    ]
                }, {
                    id:     '6',
                    name:   "trade",
                    title:  "Торговые помещения",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                        "t_a_min", "t_a_max", "b_t_sid", "gas", "elt", "h_w", "c_w", "swg"
                    ]
                }, {
                    id:     '7',
                    name:   "warehouse",
                    title:  "Склады",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                        "gas", "elt", "h_w", "c_w", "s_a", "f_a"
                    ]
                }, {
                    id:     '8',
                    name:   "business",
                    title:  "Готовый бизнес",
                    filters: [
                        "op_sid", "p_min", "p_max", "cu_sid"
                    ]
                }
            ];
        }
    }
}