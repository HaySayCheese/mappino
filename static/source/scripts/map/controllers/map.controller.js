export class MapController {
    constructor($scope, filtersService, markersService) {
        this.$scope         = $scope;
        this.filtersService = filtersService;
        this.markersService = markersService;

        this._map = null;

        google.maps.event.addDomListener(window, "load", this.initMap());

        $scope.$on('pages.map.MarkersService.MarkersIsLoaded', () => {
            markersService.place(this._map);
        });

        $scope.$on('pages.map.PlaceAutocompleteController.PlaceChanged', (event, place) => {
            this.positioningMap(place);
        });
    }



    initMap() {
        var map_options = {
            center:     new google.maps.LatLng(this.filtersService.filters.map.l.split(',')[0], this.filtersService.filters.map.l.split(',')[1]),
            zoom:       parseInt(this.filtersService.filters.map.z),
            mapTypeId:  google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true,
            styles: [{"featureType":"all","stylers":[{"saturation":0},{"hue":"#e7ecf0"}]},{"featureType":"road","stylers":[{"saturation":-70}]},{"featureType":"transit","stylers":[{"visibility":"off"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"water","stylers":[{"visibility":"simplified"},{"saturation":-60}]}]
        };

        this._map = new google.maps.Map(document.getElementById("map"), map_options);

        google.maps.event.addListener(this._map, 'idle', () => {
            this.filtersService.update('map', {
                z: this._map.getZoom(),
                v: this._map.getBounds(),
                l: this._map.getCenter().toUrlValue()
            });
        });
    }



    positioningMap(place) {
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

MapController.$inject = ['$scope', 'FiltersService', 'MarkersService'];