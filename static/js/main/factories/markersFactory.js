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
        pieMarkers = {
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
        jsonFilters = {
            zoom: "",
            viewport: "",
            filters: []
        };

    return {

        /**
         * Загрузка маркерів
         *
         * @param {object}      r_filters  Фільтри червоної панелі
         * @param {object}      b_filters  Фільтри синьої панелі
         * @param {object}      g_filters  Фільтри зеленої панелі
         * @param {object}      y_filters  Фільтри жовтої панелі
         * @param {object}      viewport   Вюпорт карти
         * @param {number}      zoom       Зум карти
         * @param {function}    callback
         */
        load: function(r_filters, b_filters, g_filters, y_filters, viewport, zoom, callback) {
            var that = this;

            jsonFilters = {
                zoom: "",
                viewport: "",
                filters: []
            };


            jsonFilters.zoom = zoom;
            jsonFilters.viewport = viewport;

            if (!_.isNull(r_filters.r_type_sid))
                that.createJsonFiltersFromString(r_filters, "red");
            else if(!_.isNull(b_filters.b_type_sid))
                that.createJsonFiltersFromString(b_filters, "blue");
            else if(!_.isNull(g_filters.g_type_sid))
                that.createJsonFiltersFromString(g_filters, "green");
            else if(!_.isNull(y_filters.y_type_sid))
                that.createJsonFiltersFromString(y_filters, "yellow");


            clearTimeout(requestTimeout);
            requestTimeout = setTimeout(function() {
                $rootScope.loadings.markers = true;
            }, 300);

            Queries.Map.getMarkers(JSON.stringify(jsonFilters)).success(function(data) {
                that.clearPanelMarkers("red");
                that.clearPanelMarkers("blue");
                that.clearPanelMarkers("green");
                that.clearPanelMarkers("yellow");


                that.add(data, function() {
                    _.isFunction(callback) && callback(markers);
                });

                clearTimeout(requestTimeout);
                $rootScope.loadings.markers = false;
            });
        },


        /**
         * Додання маркерів в масив
         *
         * @param {Array}      data   Масив який вертає сервер
         * @param {function}   callback
         */
        add: function(data, callback) {
            var that = this;

            for (var panel in data) {
                var lat = "", lng = "", latLng = "";

                if (data.hasOwnProperty(panel)) {

                    for (var marker in data[panel]) {

                        if (data[panel].hasOwnProperty(marker)) {
                            lat = marker.split(":")[0];
                            lng = marker.split(":")[1];

                            lat = parseFloat(lat);
                            lng = parseFloat(lng);

                            latLng = lat + ";" + lng;

                            // if zoom <=14
                            if (data[panel][marker].d1) {
                                that.createMarkerObject(data[panel][marker], panel, latLng);
                            } else {
                                // create markers on zoom >14
                                pieMarkers[panel][latLng] = { publication_count: parseInt(data[panel][marker]) };
                            }
                        }
                    }


                    if (lat > minLat && lng < maxLng) {
                        if (lat > nePoint.lat)
                            nePoint.lat = lat;

                        if (lng < nePoint.lng)
                            nePoint.lng = lng;
                    }
                    if (lat < maxLat && lng > minLng) {
                        if (lat < swPoint.lat)
                            swPoint.lat = lat;

                        if (lng > swPoint.lng)
                            swPoint.lng = lng;
                    }
                }
            }
            that.comparePieMarkers();

            _.isFunction(callback) && callback();
        },


        createMarkerObject: function(data, panel, latLng, tid) {
            markers[panel][latLng] = new MarkerWithLabel({
                id:             data.id,
                tid:            data.tid,
                icon:           '/static/img/markers/' + panel + '-normal.png',
                position:       new google.maps.LatLng(latLng.split(";")[0], latLng.split(";")[1]),
                labelClass:     "marker-label",
                labelAnchor:    new google.maps.Point(0, 39),
                labelContent:   data.d0 + "</br>" + data.d1,
                labelInBackground: true
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
                icon: '/static/img/markers/transparent-marker.png',
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
                labelClass: "marker-pie-chart " + sizeOfPieChart,
            });
        },

        comparePieMarkers: function() {
            var panels = {
                red: {},
                blue: {},
                green: {},
                yellow: {}
            };

            for (var panel in pieMarkers) {
                if (panel == "compared")
                    break;

                if (pieMarkers.hasOwnProperty(panel)) {
                    for (var marker in pieMarkers[panel]) {

                        if (!pieMarkers['compared'][marker] && pieMarkers[panel].hasOwnProperty(marker)) {
                            var panelName = panel + "_publication_count";

                            pieMarkers["compared"][marker] = {
                                red_publication_count:      0,
                                blue_publication_count:     0,
                                green_publication_count:    0,
                                yellow_publication_count:   0
                            };
                            pieMarkers['compared'][marker].publication_count = pieMarkers[panel][marker].publication_count;
                            pieMarkers['compared'][marker][panelName] = pieMarkers[panel][marker].publication_count;

                            for (var _panel in panels) {
                                if (_panel != panel && panels.hasOwnProperty(_panel) && pieMarkers[_panel][marker] ) {
                                    var _panelName = _panel + "_publication_count";

                                    pieMarkers["compared"][marker].publication_count += pieMarkers[_panel][marker].publication_count;
                                    pieMarkers["compared"][marker][_panelName] = pieMarkers[_panel][marker].publication_count;
                                }
                            }
                        }
                    }
                }
            }

            for (var comparedMarker in pieMarkers["compared"]) {
                var comparedMarkerPanel = pieMarkers["compared"][comparedMarker].red_publication_count ? "red" :
                                            pieMarkers["compared"][comparedMarker].blue_publication_count ? "blue" :
                                                pieMarkers["compared"][comparedMarker].green_publication_count ? "green":
                                                    pieMarkers["compared"][comparedMarker].yellow_publication_count ? "yellow" : null;

                this.createPieObject(pieMarkers["compared"][comparedMarker], comparedMarkerPanel, comparedMarker);
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

        createJsonFiltersFromString: function(filters, panel) {
            var that = this,
                stringFilters = {},
                tid = "";

            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {

                    if (key.toString().substring(2) == "type_sid") {
                        if (filters[key] == null || filters[key] == "undefined") {
                            pieMarkersLoaded[panel] = true;
                            return;
                        }

                        tid = filters[key];
                    }

                    if (filters[key] !== false && filters[key] !== "false" && filters[key] !== "" && filters[key] !== null) {
                        var param = key.toString().substring(2),
                            value = filters[key];

                        stringFilters[param] = value;
                    }
                }
            }
            stringFilters['panel'] = panel;

            jsonFilters.filters.push(stringFilters);
        },


        clearTempPieMarkers: function() {
            pieMarkers = {
                red: {},
                blue: {},
                green: {},
                yellow: {},
                compared: {}
            }
        }
    }
});