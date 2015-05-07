/// <reference path='../_references.ts' />


module pages.map {
    'use strict';

    export class MapController {
        map: any;

        public static $inject = [
            '$scope'
        ];

        constructor(private $scope) {
            $scope.$on('$stateChangeSuccess', function(prevent, current) {
                console.log(current);
                //console.log(this.map);
            });

            google.maps.event.addDomListener(window, "load", this.initMap);
        }

        private initMap() {
            this.map = new google.maps.Map(document.getElementById("map"), {
                center: new google.maps.LatLng(48.455935, 34.41285),
                zoom: 6,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                disableDefaultUI: true
            });
        }

    }
}
