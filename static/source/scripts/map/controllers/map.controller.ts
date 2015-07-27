/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class MapController {
        private _map: any;

        public static $inject = [
            '$scope',
            'FiltersService',
            'MarkersService'
        ];

        constructor(private $scope,
                    private filtersService: FiltersService,
                    private markersService: MarkersService) {
            // ---------------------------------------------------------------------------------------------------------
            var self = this;
            google.maps.event.addDomListener(window, "load", () => this.initMap(this));

            $scope.$on('Mappino.Map.MarkersService.MarkersIsLoaded', function() {
                markersService.place(self._map)
            });

            $scope.$on('Mappino.Map.PlaceAutocompleteController.PlaceChanged', function(event, place) {
                self.positioningMap(place);
            })
        }



        private initMap(self) {
            var map_options: google.maps.MapOptions = {
                center:     new google.maps.LatLng(this.filtersService.filters['map']['l'].split(',')[0], this.filtersService.filters['map']['l'].split(',')[1]),
                zoom:       parseInt(this.filtersService.filters['map']['z']),
                //mapTypeId:  google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true,
                styles: [
                    {
                        "featureType": "landscape",
                        "stylers": [
                            {
                                "hue": "#FFBB00"
                            },
                            {
                                "saturation": 43.400000000000006
                            },
                            {
                                "lightness": 37.599999999999994
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    },
                    {
                        "featureType": "road.highway",
                        "stylers": [
                            {
                                "hue": "#FFC200"
                            },
                            {
                                "saturation": -61.8
                            },
                            {
                                "lightness": 45.599999999999994
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    },
                    {
                        "featureType": "road.arterial",
                        "stylers": [
                            {
                                "hue": "#FF0300"
                            },
                            {
                                "saturation": -100
                            },
                            {
                                "lightness": 51.19999999999999
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    },
                    {
                        "featureType": "road.local",
                        "stylers": [
                            {
                                "hue": "#FF0300"
                            },
                            {
                                "saturation": -100
                            },
                            {
                                "lightness": 52
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    },
                    {
                        "featureType": "water",
                        "stylers": [
                            {
                                "hue": "#0078FF"
                            },
                            {
                                "saturation": -13.200000000000003
                            },
                            {
                                "lightness": 2.4000000000000057
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    },
                    {
                        "featureType": "poi",
                        "stylers": [
                            {
                                "hue": "#00FF6A"
                            },
                            {
                                "saturation": -1.0989010989011234
                            },
                            {
                                "lightness": 11.200000000000017
                            },
                            {
                                "gamma": 1
                            }
                        ]
                    }
                ]
            };

            self._map = new google.maps.Map(document.getElementById("map"), map_options);

            google.maps.event.addListener(self._map, 'idle', function() {
                self.filtersService.update('map', {
                    z: self._map.getZoom(),
                    v: self._map.getBounds(),
                    l: self._map.getCenter().toUrlValue()
                });
            });
        }



        private positioningMap(place: any) {
            if (!place.geometry)
                return;

            if (place.geometry.viewport) {
                this._map.fitBounds(place.geometry.viewport);
            } else {
                this._map.panTo(place.geometry.location);
                this._map.setZoom(17);
            }
        }
    }
}
