'use strict';

app.factory('Markers', function(Queries, $rootScope, $interval) {
    var markers = {
            red: {},
            blue: {},
            green: {},
            yellow: {}
        },
        tempPieMarkers = {
            red: {},
            blue: {},
            green: {},
            yellow: {},
            compared: {}
        },
        pieMarkersLoaded = {
            red:    false,
            blue:   false,
            green:  false,
            yellow: false
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
        },
        requestTimeout = null,
        pieMarkerInterval = null;

    return {

        /**
         * Загрузка маркерів
         *
         * @param {object}      filters  Фільтри
         * @param {string}      viewport Вюпорт карти
         * @param {string}      zoom     Зум карти
         * @param {string}      panel    Колір панелі фільтрів
         * @param {function}    callback
         */
        load: function(filters, viewport, zoom, panel, callback) {
            var that = this,
                tid = null,
                stringFilters = "";

            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {

                    if (key.toString().substring(2) == "type_sid") {
                        if (filters[key] == null || filters[key] == "undefined") {
                            that.clearPanelMarkers(panel);
                            pieMarkersLoaded[panel] = true;
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

            if (zoom <= 14)
                stringFilters += "&zoom=" + zoom;

            clearTimeout(requestTimeout);
            requestTimeout = setTimeout(function() {
                $rootScope.loadings.markers = true;
            }, 300);

            Queries.Map.getMarkers(tid, stringFilters, viewport).success(function(data) {
                that.clearPanelMarkers(panel);
                that.add(tid, panel, data, function() {
                    _.isFunction(callback) && callback(markers);
                });

                clearTimeout(requestTimeout);
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

            for (var marker in data) {
                var lat = "", lng = "", latLng = "";

                if (data.hasOwnProperty(marker)) {


                    if (!_.keys(data[marker]).length) {
                        pieMarkersLoaded[panel] = true;

                        for (var pieMarker in data) {
                            lat = pieMarker.split(":")[0];
                            lng = pieMarker.split(":")[1];
                            latLng = pieMarker.split(":")[0] + ";" + pieMarker.split(":")[1];

                            lat = parseFloat(lat);
                            lng = parseFloat(lng);

                            tempPieMarkers[panel][latLng] = { publication_count: parseInt(data[pieMarker]) };
                        }

                        clearInterval(pieMarkerInterval);
                        pieMarkerInterval = setInterval(function() {
                            if (pieMarkersLoaded.red && pieMarkersLoaded.blue && pieMarkersLoaded.yellow && pieMarkersLoaded.green) {
                                that.comparePieMarkers();
                                that.resetPieMarkersLoaded();
                                _.isFunction(callback) && callback();
                                clearInterval(pieMarkerInterval);
                            }
                        }, 200);

                        return;
                    }



                    lat = marker.split(":")[0];
                    lng = marker.split(":")[1];
                    latLng = marker.split(":")[0] + ";" + marker.split(":")[1];

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
                        that.createMarkerObject(data[marker], tid, panel, latLng);
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

            _.isFunction(callback) && callback();
        },


        createMarkerObject: function(data, tid, panel, latLng) {
            markers[panel][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(latLng.split(";")[0], latLng.split(";")[1]),
                tid: tid,
                id: data.id,
                icon: '/static/img/markers/' + panel + '-normal.png',
                labelInBackground: true,
                labelContent: data.d0 + "</br>" + data.d1,
                labelAnchor: new google.maps.Point(0, 40),
                labelClass: "marker-label"
            });
        },

        createPieObject: function(marker, panel, latLng) {
            var red_percent_in_deg      = (360 / 100 * ((marker.red_publication_count / marker.publication_count) * 100))   || 0,
                blue_percent_in_deg     = (360 / 100 * ((marker.blue_publication_count / marker.publication_count) * 100))  || 0,
                green_percent_in_deg    = (360 / 100 * ((marker.green_publication_count / marker.publication_count) * 100)) || 0,
                yellow_percent_in_deg   = (360 / 100 * ((marker.yellow_publication_count / marker.publication_count) * 100)) || 0,
                sizeOfPieChart = marker.publication_count < 100 ? "small" :
                                    marker.publication_count >= 100 && marker.publication_count < 1000 ? "medium" :
                                        marker.publication_count >= 1000 && marker.publication_count < 10000 ? "large" : "super-big";


            markers[panel][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(latLng.split(";")[0], latLng.split(";")[1]),
                type: "pie-marker",
                labelInBackground: true,
                labelContent:
                    "<style>" +
                        ".pie.red:before {" +
                            "transform: rotate(" + red_percent_in_deg + "deg);" +
                        "}"+
                        ".pie.blue {" +
                            "transform: rotate(" + red_percent_in_deg + "deg);" +
                        "}"+
                        ".pie.blue:before {" +
                            "transform: rotate(" + blue_percent_in_deg + "deg);" +
                        "}"+
                        ".pie.green {" +
                            "transform: rotate(" + (blue_percent_in_deg + red_percent_in_deg) + "deg);" +
                        "}"+
                        ".pie.green:before {" +
                            "transform: rotate(" + green_percent_in_deg + "deg);" +
                        "}"+
                        ".pie.yellow {" +
                            "transform: rotate(" + (yellow_percent_in_deg + green_percent_in_deg + blue_percent_in_deg) + "deg);" +
                        "}"+
                        ".pie.yellow:before {" +
                            "transform: rotate(" + yellow_percent_in_deg + "deg);" +
                        "}"+
                    "</style>"+
                    "<div>" +
                        "<div class='marker-pie-chart-inner'>" + marker.publication_count + "</div>" +
                        "<div class='pie red'></div>" +
                        "<div class='pie blue'></div>" +
                        "<div class='pie green'></div>" +
                        "<div class='pie yellow'></div>" +
                    "</div>",
                labelAnchor: new google.maps.Point(30, 45),
                labelClass: "marker-pie-chart " + sizeOfPieChart

            });
        },

        comparePieMarkers: function() {
            for (var panel in tempPieMarkers) {
                for (var marker in tempPieMarkers[panel]) {
                    if (panel == "red") {
                        tempPieMarkers["compared"][marker] = {
                            publication_count:          tempPieMarkers["red"][marker].publication_count,
                            red_publication_count:      tempPieMarkers["red"][marker].publication_count,
                            blue_publication_count:     0,
                            green_publication_count:    0,
                            yellow_publication_count:   0
                        };

                        if (tempPieMarkers["blue"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count = tempPieMarkers["compared"][marker].publication_count + tempPieMarkers["blue"][marker].publication_count;
                            tempPieMarkers["compared"][marker].blue_publication_count = tempPieMarkers["blue"][marker].publication_count;

                            delete tempPieMarkers["blue"][marker];
                        }
                        if (tempPieMarkers["green"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count = tempPieMarkers["compared"][marker].publication_count + tempPieMarkers["green"][marker].publication_count;
                            tempPieMarkers["compared"][marker].green_publication_count = tempPieMarkers["green"][marker].publication_count;

                            delete tempPieMarkers["green"][marker];
                        }
                        if (tempPieMarkers["yellow"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count = tempPieMarkers["compared"][marker].publication_count + tempPieMarkers["yellow"][marker].publication_count;
                            tempPieMarkers["compared"][marker].yellow_publication_count = tempPieMarkers["yellow"][marker].publication_count;

                            delete tempPieMarkers["yellow"][marker];
                        }
                        delete tempPieMarkers[panel][marker];
                    }
                }
            }

            for (var comparedMarker in tempPieMarkers["compared"]) {
                var comparedMarkerPanel = tempPieMarkers["compared"][comparedMarker].red_publication_count ? "red" :
                                            tempPieMarkers["compared"][comparedMarker].blue_publication_count ? "blue" :
                                                tempPieMarkers["compared"][comparedMarker].green_publication_count ? "green":
                                                    tempPieMarkers["compared"][comparedMarker].yellow_publication_count ? "yellow" : null;

                this.createPieObject(tempPieMarkers["compared"][comparedMarker], comparedMarkerPanel, comparedMarker);
            }

            this.clearTempPieMarkers();
        },

        clearPanelMarkers: function(panel) {
            for (var marker in markers[panel]) {
                if (markers[panel].hasOwnProperty(marker)) {
                    markers[panel][marker].setMap(null);
                    delete markers[panel][marker];
                }
            }
        },


        resetPieMarkersLoaded: function() {
            pieMarkersLoaded = {
                red:    false,
                blue:   false,
                green:  false,
                yellow: false
            }
        },


        clearTempPieMarkers: function() {
            tempPieMarkers = {
                red: {},
                blue: {},
                green: {},
                yellow: {},
                compared: {}
            }
        }

        /*
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
        */
    }

});