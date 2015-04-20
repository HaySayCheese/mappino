app.factory('PublicationTypesFactory', function() {
    "use strict";

    var publicationTypes = [
        { name: "flat", id: 0, title: "Квартиры",
            filters: [
                "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                "msd", "grd", "pl_sid", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
            ]
        },
        { name: "house", id: 1, title: "Дома",
            filters: [
                "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                "s_m", "fml", "frg", "r_c_min", "r_c_max", "f_c_min", "f_c_max", "elt", "h_w",
                "gas", "c_w", "swg", "h_t_sid"
            ]
        },
        { name: "room", id: 2, title: "Комнаты",
            filters: [
                "op_sid", "pr_sid", "p_min", "p_max", "cu_sid", "p_c_min", "p_c_max", "n_b",
                "s_m", "fml", "frg", "r_c_min", "r_c_max", "t_a_min", "t_a_max", "f_min", "f_max",
                "msd", "grd", "lft", "elt", "h_w", "c_w", "gas", "h_t_sid"
            ]
        },
        { name: "land", id: 3, title: "Земельные участки",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid", "a_min", "a_max", "gas", "elt", "wtr", "swg"
            ]
        },
        { name: "garage", id: 4, title: "Гаражи",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid", "t_a_min", "t_a_max"
            ]
        },
        { name: "office", id: 5, title: "Офисы",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "t_a_min", "t_a_max",
                "c_c_min", "c_c_max", "sct", "ktn", "h_w", "c_w"
            ]
        },
        { name: "trade", id: 6, title: "Торговые помещения",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                "t_a_min", "t_a_max", "b_t_sid", "gas", "elt", "h_w", "c_w", "swg"
            ]
        },
        { name: "warehouse", id: 7, title: "Склады",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid", "n_b", "s_m", "h_a_min", "h_a_max",
                "gas", "elt", "h_w", "c_w", "s_a", "f_a"
            ]
        },
        { name: "business", id: 8, title: "Готовый бизнес",
            filters: [
                "op_sid", "p_min", "p_max", "cu_sid"
            ]
        }
    ];

    return {
        getPublicationTypes: function() {
            return publicationTypes;
        },


        getAvailableTypeFiltersById: function(id) {
            return _.where(publicationTypes, { 'id': id })[0].filters;
        }
    };
});