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
         * @param {string}      viewport Вюпорт карти
         * @param {function}    callback
         */
        load: function(viewport, callback) {
            var that = this;

            mapQueries.getMarkers(viewport).success(function(data) {
                that.add(data, function() {
                    _.isFunction(callback) && callback(markers);
                });
            });
        },


        /**
         * Додання маркерів в масив
         *
         * @param {Array}      data Масив який вертає сервер
         * @param {function}   callback
         */
        add: function(data, callback) {
            this.clear();

            _.each(data, function(_tid, key) {
                var markerTid  = key,
                    markerLat  = "",
                    markerLng  = "",
                    markerIcon = "";

                _.map(_tid, function(_markers, mkey) {
                    _.each(_markers, function(_marker, key) {
                        markerLat = _.first(mkey.split(";")) + "." + _.first(key.split(":"));
                        markerLng = _.last(mkey.split(";")) + "." + _.last(key.split(":"));

                        markers.push(new MarkerWithLabel({
                            position: new google.maps.LatLng(markerLat, markerLng),

                            tid: markerTid,
                            id: _marker.id,

                            labelInBackground: true,
                            labelContent: "4 комн. </br> 25 000 грн.",
                            labelAnchor: new google.maps.Point(0, 40),
                            labelClass: "marker-label"
                        }));
                    })

                });
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