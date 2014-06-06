'use strict';

app.factory('Markers', function(mapQueries, $rootScope) {
    var markers = {
            red: {},
            blue: {},
            green: {},
            yellow: {}
        };

    return {

        /**
         * Загрузка маркерів
         *
         * @param {object}      filters  Фільтри
         * @param {string}      viewport Вюпорт карти
         * @param {string}      panel    Колір панелі фільтрів
         * @param {function}    callback
         */
        load: function(filters, viewport, panel, callback) {
            var that = this,
                tid = null,
                stringFilters = "";

            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {

                    if (key.toString().substring(2) == "type_sid") {
                        if (filters[key] == null || filters[key] == "undefined") {
                            that.clearPanelMarkers(panel);
                            return;
                        }

                        tid = filters[key];
                    }

                    if (filters[key] !== false && filters[key] !== "false" && filters[key] !== "" && filters[key] !== null) {
                        var param = "&" + key.toString().substring(2),
                            value = "=" + filters[key];

                        stringFilters += param + value;
                    }
                }
            }

            $rootScope.loaders.markers = true;
            mapQueries.getMarkers(tid, stringFilters, viewport).success(function(data) {
                that.clearPanelMarkers(panel);
                that.add(tid, panel, data, function() {
                    _.isFunction(callback) && callback(markers);
                });

                $rootScope.loaders.markers = false;
            });
        },


        /**
         * Додання маркерів в масив
         *
         * @param {number}     tid    Тип обєкта
         * @param {string}     panel  Колір панелі фільтрів
         * @param {Array}      data   Масив який вертає сервер
         * @param {function}   callback
         */
        add: function(tid, panel, data, callback) {
            var that = this;

            for (var d_key in data) {
                var latLng = "";

                if (data.hasOwnProperty(d_key)) {

                    if (!_.keys(data[d_key]).length)
                        return;

                    for (var c_key in data[d_key]) {

                        if (data[d_key].hasOwnProperty(c_key)) {
                            latLng = d_key.split(";")[0] + "." + c_key.split(":")[0] + ";" + d_key.split(";")[1] + "." + c_key.split(":")[1];

                            if (panel != "red" && markers["red"][latLng]) {
                                return;
                            } else if (panel != "blue" && markers["blue"][latLng]) {
                                return;
                            } else if (panel != "green" && markers["green"][latLng]) {
                                return;
                            } else if (panel != "yellow" && markers["yellow"][latLng]) {
                                return;
                            } else if(!markers[panel][latLng]) {
                                that.createMarkerObject(data[d_key][c_key], tid, panel, latLng);
                            } else {
                                return;
                            }
                        }
                    }
                }
            }

            _.isFunction(callback) && callback();
        },


        createMarkerObject: function(data, tid, panel, latLng) {
            markers[panel][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(latLng.split(";")[0], latLng.split(";")[1]),
                tid: tid,
                id: data.id,
                icon: '/mappino_static/img/markers/' + panel + '-normal.png',
                labelInBackground: true,
                labelContent: data.d0 + "</br>" + data.d1,
                labelAnchor: new google.maps.Point(0, 40),
                labelClass: "marker-label"
            });
        },

        clearPanelMarkers: function(panel) {
            for (var marker in markers[panel]) {
                if (markers[panel].hasOwnProperty(marker)) {
                    markers[panel][marker].setMap(null);
                    delete markers[panel][marker];
                }
            }
        }
    }

});