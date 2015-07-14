/// <reference path='../_all.ts' />


module mappino.cabinet {
    export class UnpublishedPublicationController {
        private map: google.maps.Map;
        private marker: google.maps.Marker;

        private placeAutocompleteField: any;
        private placeAutocomplete: google.maps.places.Autocomplete;

        private _publication: Object = {};

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            '$timeout',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: angular.ui.IStateService,
                    private $timeout: angular.ITimeoutService,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------
            this._publication['tid']    = $state.params['id'].split(':')[0];
            this._publication['hid']    = $state.params['id'].split(':')[1];

            $scope.activeTabStateIndex = 0;

            $scope.publication = {};


            this.loadPublicationData();
        }



        private publish() {
            if (this.$scope.publicationForm.$invalid) {
                var checkboxElement = angular.element("input[type='checkbox'].ng-invalid")[0],
                    inputElement    = angular.element("textarea.ng-invalid, input.ng-invalid")[0];

                if (checkboxElement) {
                    this.$scope.activeTabStateIndex = 1;
                    checkboxElement.parentNode.scrollIntoView(true);
                } else {
                    if (inputElement.id == "publication-map-input")
                        this.$scope.activeTabStateIndex = 2;
                    else
                        this.$scope.activeTabStateIndex = 0;

                    inputElement.focus();
                }

                return;
            } else {
                this.publicationsService.publish(this._publication, () => {

                });
            }
        }



        public uploadPublicationPhotos($files) {
            this.publicationsService.uploadPublicationPhotos(this._publication, $files, (response) => {
                console.log(response)
            })
        }




        private loadPublicationData() {
            this.$rootScope.loaders.base = true;

            this.publicationsService.loadPublication(this._publication, (response) => {
                this.$scope.publication = response;
                this.$rootScope.loaders.base = false;

                this.initInputsChange();
                this.initMap()
            });
        }



        private initMap() {
            this.$timeout(() => {
                var center = new google.maps.LatLng(this.$scope.publication.head.lat || 50.448159, this.$scope.publication.head.lng || 30.524654);

                var mapOptions = {
                    center: center,
                    zoom: this.$scope.publication.head.lat ? 17 : 8,
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    mapTypeControl: false,
                    streetViewControl: false,
                    scrollwheel: true,
                    disableDoubleClickZoom: false
                },
                autocompleteOptions = {
                    componentRestrictions: {
                        country: "ua"
                    }
                };

                this.placeAutocompleteField = document.getElementById("publication-map-input");
                this.placeAutocomplete = new google.maps.places.Autocomplete(<HTMLInputElement>this.placeAutocompleteField, autocompleteOptions);

                this.map = new google.maps.Map(document.getElementById("publication-map"), mapOptions);

                this.marker = new google.maps.Marker({
                    map: this.map,
                    draggable: true,
                    position: center
                });

                this.placeAutocomplete.bindTo('bounds', this.map);


                google.maps.event.addListener(this.map, 'click', (e) => {
                    this.marker.setPosition(e.latLng);
                    this.setAddressFromLatLng(e.latLng, this.placeAutocompleteField);
                });
                google.maps.event.addListener(this.marker, 'dragend', (e) => {
                    this.setAddressFromLatLng(e.latLng, this.placeAutocompleteField);
                });
                google.maps.event.addListener(this.placeAutocomplete, 'place_changed', () => {
                    var place = this.placeAutocomplete.getPlace();

                    if (!place.geometry) return;

                    if (place.geometry.viewport) {
                        this.map.fitBounds(place.geometry.viewport);
                    } else {
                        this.map.panTo(place.geometry.location);
                        this.marker.setPosition(place.geometry.location);
                        this.map.setZoom(17);
                        this.setAddressFromLatLng(place.geometry.location, this.placeAutocompleteField);
                    }
                });
                google.maps.event.addListenerOnce(this.map, 'idle', (e) => {
                    this.$timeout(() => {
                        var latLng = new google.maps.LatLng(this.$scope.publication.head.lat || 50.448159, this.$scope.publication.head.lng || 30.524654);
                        this.map.setCenter(latLng);
                        this.publicationsService.checkField(this._publication, { f: "lat_lng", v: latLng.lat() + ";" + latLng.lng() });
                    }, 1000);
                });
            }, 1000)
        }



        private setAddressFromLatLng(latLng: google.maps.LatLng, input: HTMLInputElement) {
            var geocoder = new google.maps.Geocoder();

            geocoder.geocode({ 'latLng': latLng }, (results, status) => {
                if(status == google.maps.GeocoderStatus.OK)
                    angular.element(input).val(results[0].formatted_address);

                angular.element(input).trigger("input");

                this.publicationsService.checkField(this._publication, { f: "address", v: input.value }, null);
                this.publicationsService.checkField(this._publication, { f: "lat_lng", v: latLng.lat() + ";" + latLng.lng() }, null);
            });
        }



        private initInputsChange() {
            angular.element("form[name='publicationForm'] input, form[name='publicationForm'] textarea").bind("focusout", (e) => {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.publicationForm[name].$dirty) {
                    return;
                }

                this.publicationsService.checkField(this._publication, { f: name, v: value }, (newValue) => {
                    if (newValue && !angular.element(e.currentTarget).is(":focus")) {
                        e.currentTarget['value'] = newValue;
                    }

                    this.$scope.publicationForm[name].$setValidity("invalid", true);
                }, (response) => {
                    this.$scope.publicationForm[name].$setValidity("invalid", response.code === 0);
                });
            });

            angular.element(".publication-view-container input[type='checkbox']").bind("change", function(e) {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['checked'];

                this.publicationsService.checkField(this._publication, { f: name, v: value });
            });
        }


        private checkField(elementName) {
            var elementValue = null;

            this.validatePublicationOperation();

            if (elementName.indexOf('rent_') !== -1) {
                elementValue = this.$scope.publication.rent_terms[elementName.replace('rent_', '')];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (elementName.indexOf('sale_') !== -1) {
                elementValue = this.$scope.publication.sale_terms[elementName.replace('sale_', '')];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.head[elementName])) {
                elementValue = this.$scope.publication.head[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.body[elementName])) {
                elementValue = this.$scope.publication.body[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.rent_terms[elementName])) {
                elementValue = this.$scope.publication.rent_terms[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });

            } else if (!_.isUndefined(this.$scope.publication.sale_terms[elementName])) {
                elementValue = this.$scope.publication.sale_terms[elementName];
                this.publicationsService.checkField(this._publication, { f: elementName, v: elementValue });
            }
        }



        private validatePublicationOperation() {
            if (this.$scope.publication.head.for_sale == false && this.$scope.publication.head.for_rent == false) {
                this.$scope.publication.head.for_sale = true;
                this.checkField('for_sale');
            }
        }



        private changeState(state: string) {
            if (state == 'next') this.$scope.activeTabStateIndex++;

            else if (state == 'prev') this.$scope.activeTabStateIndex--;

            else this.$scope.activeTabStateIndex = state;

            angular.element('main').animate({
                scrollTop: 0
            }, 'fast');
        }
    }
}