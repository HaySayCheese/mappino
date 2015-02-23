'use strict';

app.factory('Markers', function(Queries, $rootScope, $interval, uuid) {
    var markers = {
            red: {},
            blue: {},
            green: {},
            yellow: {}
        },
        tempMarkers = {
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
        pieMarkerInterval = null,
        jsonFilters = {
            zoom: "",
            viewport: "",
            filters: []
        };

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
        load: function(r_filters, b_filters, g_filters, y_filters, viewport, zoom, callback) {
            var that = this,
                tid = null,
                stringFilters = "";

            jsonFilters = {
                zoom: "",
                viewport: "",
                filters: []
            };

            jsonFilters.zoom = zoom;
            jsonFilters.viewport = viewport;

            that.createJsonFiltersFromString(r_filters);
            that.createJsonFiltersFromString(b_filters);
            that.createJsonFiltersFromString(g_filters);
            that.createJsonFiltersFromString(y_filters);

            console.log("load");
            console.log(jsonFilters);

            clearTimeout(requestTimeout);
            requestTimeout = setTimeout(function() {
                $rootScope.loadings.markers = true;
            }, 300);

            console.log(JSON.stringify(jsonFilters))
            Queries.Map.getMarkers(JSON.stringify(jsonFilters).replace("/\"/g", 'ppp')).success(function(data) {
                that.clearPanelMarkers(panel, function() {
                    that.add(tid, panel, data, function() {

                        _.isFunction(callback) && callback(markers);
                        console.log(markers)
                    });

                    clearTimeout(requestTimeout);
                    $rootScope.loadings.markers = false;
                });
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
            var _uuid = uuid.new(),

                red_percent_in_deg      = Math.round((360 / 100 * ((marker.red_publication_count / marker.publication_count) * 100))      || 0),
                blue_percent_in_deg     = Math.round((360 / 100 * ((marker.blue_publication_count / marker.publication_count) * 100))     || 0),
                green_percent_in_deg    = Math.round((360 / 100 * ((marker.green_publication_count / marker.publication_count) * 100))    || 0),
                yellow_percent_in_deg   = Math.round((360 / 100 * ((marker.yellow_publication_count / marker.publication_count) * 100))   || 0),

                redAdditionalClass      = red_percent_in_deg > 180 ? ' full' : '',
                blueAdditionalClass     = blue_percent_in_deg > 180 ? ' full' : '',
                greenAdditionalClass    = green_percent_in_deg > 180 ? ' full' : '',
                yellowAdditionalClass   = yellow_percent_in_deg > 180 ? ' full' : '',

                sizeOfPieChart = marker.publication_count < 100 ? "small" :
                                    marker.publication_count >= 100 && marker.publication_count < 1000 ? "medium" :
                                        marker.publication_count >= 1000 && marker.publication_count < 10000 ? "large" : "super-big";


            markers[panel][latLng] = new MarkerWithLabel({
                position: new google.maps.LatLng(latLng.split(";")[0], latLng.split(";")[1]),
                type: "pie-marker",
                labelInBackground: false,
                labelContent:
                    "<style>" +
                        "." + _uuid + ".pie.red {" +
                            "transform: rotate(0deg);" +
                        "}"+
                        "." + _uuid + ".pie.red:before {" +
                            "transform: rotate(" + red_percent_in_deg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.blue {" +
                            "transform: rotate(" + red_percent_in_deg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.blue:before {" +
                            "transform: rotate(" + blue_percent_in_deg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.green {" +
                            "transform: rotate(" + (blue_percent_in_deg + red_percent_in_deg) + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.green:before {" +
                            "transform: rotate(" + green_percent_in_deg + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.yellow {" +
                            "transform: rotate(" + (yellow_percent_in_deg + green_percent_in_deg + blue_percent_in_deg) + "deg);" +
                        "}"+
                        "." + _uuid + ".pie.yellow:before {" +
                            "transform: rotate(" + yellow_percent_in_deg + "deg);" +
                        "}"+
                    "</style>"+
                    "<div>" +
                        "<div class='marker-pie-chart-inner'>" + marker.publication_count + "</div>" +
                        "<div class='" + _uuid + " pie red" + redAdditionalClass + "'></div>" +
                        "<div class='" + _uuid + " pie blue" + blueAdditionalClass + "'></div>" +
                        "<div class='" + _uuid + " pie green" + greenAdditionalClass + "'></div>" +
                        "<div class='" + _uuid + " pie yellow" + yellowAdditionalClass + "'></div>" +
                    "</div>",
                labelAnchor: new google.maps.Point(30, 45),
                labelClass: "marker-pie-chart " + sizeOfPieChart
            });
        },

        comparePieMarkers: function() {
            for (var panel in tempPieMarkers) {
                for (var marker in tempPieMarkers[panel]) {
                    if (panel == "red") {
                        if (!tempPieMarkers["compared"][marker])
                            tempPieMarkers["compared"][marker] = {
                                publication_count:          tempPieMarkers[panel][marker].publication_count,
                                red_publication_count:      tempPieMarkers[panel][marker].publication_count,
                                blue_publication_count:     0,
                                green_publication_count:    0,
                                yellow_publication_count:   0
                            };

                        if (tempPieMarkers["blue"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["blue"][marker].publication_count;
                            tempPieMarkers["compared"][marker].blue_publication_count = tempPieMarkers["blue"][marker].publication_count;

                            delete tempPieMarkers["blue"][marker];
                        }
                        else if (tempPieMarkers["green"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["green"][marker].publication_count;
                            tempPieMarkers["compared"][marker].green_publication_count = tempPieMarkers["green"][marker].publication_count;

                            delete tempPieMarkers["green"][marker];
                        }
                        else if (tempPieMarkers["yellow"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["yellow"][marker].publication_count;
                            tempPieMarkers["compared"][marker].yellow_publication_count = tempPieMarkers["yellow"][marker].publication_count;

                            delete tempPieMarkers["yellow"][marker];
                        } else {
                            delete tempPieMarkers["red"][marker];
                        }
                    }

                    if (panel == "blue") {
                        if (!tempPieMarkers["compared"][marker])
                            tempPieMarkers["compared"][marker] = {
                                publication_count:          tempPieMarkers["blue"][marker].publication_count,
                                red_publication_count:      0,
                                blue_publication_count:     tempPieMarkers["blue"][marker].publication_count,
                                green_publication_count:    0,
                                yellow_publication_count:   0
                            };

                        if (tempPieMarkers["red"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["red"][marker].publication_count;
                            tempPieMarkers["compared"][marker].red_publication_count = tempPieMarkers["red"][marker].publication_count;

                            delete tempPieMarkers["red"][marker];
                        }
                        else if (tempPieMarkers["green"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["green"][marker].publication_count;
                            tempPieMarkers["compared"][marker].green_publication_count = tempPieMarkers["green"][marker].publication_count;

                            delete tempPieMarkers["green"][marker];
                        }
                        else if (tempPieMarkers["yellow"][marker]) {
                            tempPieMarkers["compared"][marker].publication_count += tempPieMarkers["yellow"][marker].publication_count;
                            tempPieMarkers["compared"][marker].yellow_publication_count = tempPieMarkers["yellow"][marker].publication_count;

                            delete tempPieMarkers["yellow"][marker];
                        } else {
                            delete tempPieMarkers["blue"][marker];
                        }
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

        clearPanelMarkers: function(panel, callback) {
            for (var marker in markers[panel]) {
                if (markers[panel].hasOwnProperty(marker)) {
                    markers[panel][marker].setMap(null);
                    delete markers[panel][marker];
                }
            }

            _.isFunction(callback) && callback();
        },

        createJsonFiltersFromString: function(filters) {
            var that = this,
                stringFilters = "",
                tid = "";

            console.log(filters)

            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {

                    if (key.toString().substring(2) == "type_sid") {
                        if (filters[key] == null || filters[key] == "undefined") {
                            //that.clearPanelMarkers(panel, function () {
                            //    pieMarkersLoaded[panel] = true;
                            //});
                            return;
                        }

                        tid = filters[key];
                        console.log(tid)
                    }

                    if (filters[key] !== false && filters[key] !== "false" && filters[key] !== "" && filters[key] !== null) {
                        var param = "," + key.toString().substring(2),
                            value = ":" + filters[key];

                        stringFilters += param + value;
                    }
                }
            }

            var tidItem = {};
            tidItem[tid] = stringFilters;
            //if (!jsonFilters.filters[tid])
                jsonFilters.filters.push(tidItem);

            console.log("createJsonFiltersFromString")
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