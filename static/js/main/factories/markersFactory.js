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
         * @param {number}      tid      Тип обєкта
         * @param {function}    callback
         */
        load: function(filters, viewport, tid, callback) {
            var that = this;

            if (filters) {
                var stringFilters = "";

                for (var key in filters) {
                    if (filters.hasOwnProperty(key) )
                        stringFilters += "&" + key.toString().substring(2) + "=" + filters[key];
                }
                console.log(stringFilters)
                mapQueries.getMarkersOfFilters(stringFilters, viewport, tid).success(function(data) {
                    that.add(data, tid, function() {
                        _.isFunction(callback) && callback(markers);
                    });
                });
            } else {
                mapQueries.getMarkers(viewport, tid).success(function(data) {
                    that.add(data, tid, function() {
                        _.isFunction(callback) && callback(markers);
                    });
                });
            }
        },


        /**
         * Додання маркерів в масив
         *
         * @param {Array}      data Масив який вертає сервер
         * @param {number}     tid      Тип обєкта
         * @param {function}   callback
         */
        add: function(data, tid, callback) {
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