'use strict';

app.factory('Markers', function(Queries, $rootScope) {
    var markers = {
            red: {},
            blue: {},
            green: {},
            yellow: {}
        },
        maxLat = 90,
        minLat = -90,
        maxLng = 180,
        minLng = -180,
        nePoint = {
            lat: minLat,
            lng: maxLng
        },
        swPoint= {
            lat: maxLat,
            lng: minLng
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

            $rootScope.loadings.markers = true;
            Queries.Map.getMarkers(tid, stringFilters, viewport).success(function(data) {
                that.clearPanelMarkers(panel);
                that.add(tid, panel, data, function() {
                    _.isFunction(callback) && callback(markers);
                });

                $rootScope.loadings.markers = false;
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
                var lat = "", lng = "", latLng = "";

                if (data.hasOwnProperty(d_key)) {

                    if (!_.keys(data[d_key]).length)
                        return;

                    for (var c_key in data[d_key]) {
                        if (data[d_key].hasOwnProperty(c_key)) {
                            lat = d_key.split(";")[0] + "." + c_key.split(":")[0];
                            lng = d_key.split(";")[1] + "." + c_key.split(":")[1];
                            latLng = lat + ";" + lng;

                            lat = parseFloat(lat);
                            lng = parseFloat(lng);

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



                            if (lat > minLat && lng < maxLng){
                                if (lat > nePoint.lat)
                                    nePoint.lat = lat;

                                if (lng < nePoint.lng)
                                    nePoint.lng = lng;
                            }
                            if (lat < maxLat && lng > minLng){
                                if (lat < swPoint.lat)
                                    swPoint.lat = lat;

                                if (lng > swPoint.lng)
                                    swPoint.lng = lng;
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
                icon: 'http://code-418.com/mappino_static/img/markers/' + panel + '-normal.png',
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
        },


        getRealtorsData: function(realtor, callback) {
            Queries.Map.getRealtorData(realtor).success(function(data) {
                _.isFunction(callback) && callback(data);
            })
        },


        getRealtorsMarkers: function(tid, realtor, callback) {
            var that = this;

            Queries.Map.getRealtorMarkers(tid, realtor).success(function(data) {
                that.clearPanelMarkers("red");
                that.add(tid, "red", data, function() {
                    _.isFunction(callback) && callback(markers);
                });
            })
        },

        getViewport: function() {
            return new google.maps.LatLngBounds(new google.maps.LatLng(nePoint.lat, nePoint.lng), new google.maps.LatLng(swPoint.lat, swPoint.lng));
        }
    }

});