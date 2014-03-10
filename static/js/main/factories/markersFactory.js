'use strict';

app.factory('Markers', function(mapQueries) {
    var markers = [],
        icons = {
            blue: ""
        };

    return {

        /**
         * Загрузка маркерів
         *
         * @param {object}      filters  Фільтри
         * @param {string}      viewport Вюпорт карти
         * @param {function}    callback
         */
        load: function(filters, viewport, callback) {
            var that = this,
                tid = null,
                stringFilters = "";

            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {

                    if (key.toString().substring(2) == "type_sid") {
                        if (filters[key] == null || filters[key] == "undefined")
                            return;

                        tid = filters[key];
                    }

                    if (filters[key] !== false && filters[key] !== "false" && filters[key] !== "" && filters[key] !== null) {
                        var param = "&" + key.toString().substring(2),
                            value = "=" + filters[key];

                        stringFilters += param + value;
                    }
                }
            }



            mapQueries.getMarkers(tid, stringFilters, viewport).success(function(data) {
                that.add(tid, data, function() {
                    _.isFunction(callback) && callback(markers);
                });
            });
        },


        /**
         * Додання маркерів в масив
         *
         * @param {Array}      data Масив який вертає сервер
         * @param {number}     tid      Тип обєкта
         * @param {function}   callback
         */
        add: function(tid, data, callback) {
            this.clear();

            _.map(data, function(_markers, mkey) {
                var markerLat  = "",
                    markerLng  = "";

                _.each(_markers, function(_marker, key) {
                    markerLat = _.first(mkey.split(";")) + "." + _.first(key.split(":"));
                    markerLng = _.last(mkey.split(";")) + "." + _.last(key.split(":"));

                    markers.push(new MarkerWithLabel({
                        position: new google.maps.LatLng(markerLat, markerLng),

                        tid: tid,
                        id: _marker.id,

                        labelInBackground: true,
                        labelContent: _marker.d0 + "</br>" + _marker.d1,
                        labelAnchor: new google.maps.Point(0, 40),
                        labelClass: "marker-label"
                    }));
                })

            });

            _.isFunction(callback) && callback();
        },


        clear: function() {
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            markers.length = 0;
        }

    }


});