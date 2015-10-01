namespace Mappino.Cabinet.Users {
    export class UnpublishedPublicationController {
        private map: google.maps.Map;
        private marker: google.maps.Marker;

        private placeAutocompleteField: any;
        private placeAutocomplete: google.maps.places.Autocomplete;

        private publication: IPublication;

        private tempPublicationPhotos: Array<Object> = [];

        private publicationIds: any = {
            tid: null,
            hid: null
        };

        public static $inject = [
            '$scope',
            '$rootScope',
            '$state',
            '$timeout',
            '$mdDialog',
            'TXT',
            'MAP',
            'PublicationsService',
        ];

        constructor(private $scope: any,
                    private $rootScope: any,
                    private $state: ng.ui.IStateService,
                    private $timeout: ng.ITimeoutService,
                    private $mdDialog: any,
                    private TXT: any,
                    private MAP: any,
                    private publicationsService: PublicationsService) {
            // ---------------------------------------------------------------------------------------------------------

            this.publicationIds.tid = $state.params['publication_id'].split(':')[0];
            this.publicationIds.hid = $state.params['publication_id'].split(':')[1];

            $scope.tempPublicationPhotos = this.tempPublicationPhotos;
            $scope.publicationPhotoLoader = {};
            $scope.forms = {};
            $scope.publicationPhotosErrors = {
                minimumPhotos: false,
                photoTooSmall: false,
                photoTooLarge: false,
            };

            angular.element(document).ready(() => {
                this.initInputsChange();
                this.initMap();
            });
        }



        public removePublication($event) {
            var confirm = this.$mdDialog.confirm()
                .parent(angular.element(document.body))
                .title(this.TXT.DIALOGS.REMOVE_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.REMOVE_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.REMOVE_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.REMOVE_PUBLICATION.OK_BTN)
                .cancel(this.TXT.DIALOGS.REMOVE_PUBLICATION.CANCEL_BTN)
                .targetEvent($event);

            this.$mdDialog.show(confirm).then(() => {
                this.$rootScope.loaders.overlay = true;
                this.publicationsService.remove(this.publicationIds)
                    .success(response => {
                    this.$rootScope.loaders.overlay = false;
                    this.$state.go('publications');
                })
                    .error(response => {
                    this.$rootScope.loaders.overlay = false;
                })
            });
        }



        public publishPublication($event) {
            if (this.$scope.forms.publicationForm.$invalid) {
                var checkboxElement = angular.element("input[type='checkbox'].ng-invalid")[0],
                    inputElement    = angular.element("textarea.ng-invalid, input.ng-invalid")[0];

                if (checkboxElement) {
                    checkboxElement.scrollIntoView(true);
                } else {
                    inputElement.scrollIntoView(true);
                    inputElement.focus();
                }
            } else if (!this.$scope.publication.photos || !this.$scope.publication.photos.length) {
                this.scrollToBottom();
            } else {
                this.$rootScope.loaders.overlay = true;

                this.publicationsService.publish(this.publicationIds)
                    .success(response => {
                        if (response.code == 3) {
                            this.$scope.publicationPhotosErrors.minimumPhotos = true;
                            this.$rootScope.loaders.overlay = false;
                            return;
                        }
                        this.$rootScope.loaders.overlay = false;
                        this.$state.go('publications');
                })
                .error(response => {
                    this.$rootScope.loaders.overlay = false;
                })
            }
        }



        public doneEditingLaterPublication($event) {
            var alert = this.$mdDialog.alert()
                .parent(angular.element(document.body))
                .clickOutsideToClose(false)
                .title(this.TXT.DIALOGS.DONE_EDITING_LATER_PUBLICATION.TITLE)
                .content(this.TXT.DIALOGS.DONE_EDITING_LATER_PUBLICATION.BODY)
                .ariaLabel(this.TXT.DIALOGS.DONE_EDITING_LATER_PUBLICATION.ARIA_LABEL)
                .ok(this.TXT.DIALOGS.DONE_EDITING_LATER_PUBLICATION.OK_BTN)
                .targetEvent($event);

            this.$mdDialog.show(alert).then(() => {
                this.$state.go('publications');
            });
        }



        public uploadPublicationPhotos($files) {
            if ($files && $files.length) {
                for (var i = 0; i < $files.length; i++) {
                    var file = $files[i];

                    this.$scope.tempPublicationPhotos.push({});
                    this.scrollToBottom();

                    this.publicationsService.uploadPhoto(this.publicationIds,file)
                        .success(response => {
                            this.$scope.tempPublicationPhotos.shift();
                            this.scrollToBottom();
                        })
                        .error(response => {
                            this.$scope.tempPublicationPhotos.shift();

                            response.code == 4 && (this.$scope.publicationPhotosErrors.photoTooLarge = true);
                            response.code == 5 && (this.$scope.publicationPhotosErrors.photoTooSmall = true);
                        })
                }
            }

            this.$scope.publicationPhotosErrors.minimumPhotos = false;
            this.$scope.publicationPhotosErrors.photoTooSmall = false;
            this.$scope.publicationPhotosErrors.photoTooLarge = false;
        }



        public removePublicationPhoto(photoId) {
            this.$scope.publicationPhotoLoader[photoId] = true;

            this.publicationsService.removePhoto(this.publicationIds, photoId)
                .success(response => {
                    this.$scope.publicationPhotoLoader[photoId] = false;
                })
        }



        public setTitlePhoto(photoId) {
            this.$scope.publicationPhotoLoader[photoId] = true;

            this.publicationsService.setTitlePhoto(this.publicationIds, photoId)
                .success(response => {
                this.$scope.publicationPhotoLoader[photoId] = false;
            })
        }



        private initMap() {
            this.$timeout(() => {
                var center = new google.maps.LatLng(this.$scope.publication.head.lat || 50.448159, this.$scope.publication.head.lng || 30.524654);

                var mapOptions: google.maps.MapOptions = {
                        center: center,
                        zoom: this.$scope.publication.head.lat ? 17 : 8,
                        mapTypeId: google.maps.MapTypeId['ROADMAP'],
                        disableDefaultUI: true,

                        zoomControl: true,
                        zoomControlOptions: {
                            position: google.maps.ControlPosition.LEFT_BOTTOM
                        },

                        mapTypeControl: true,
                        mapTypeControlOptions: {
                            position: google.maps.ControlPosition.BOTTOM_LEFT
                        },

                        styles: this.MAP.STYLES
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
                        this.publicationsService.checkField(this.publicationIds, { fieldName: "lat_lng", fieldValue: latLng.lat() + ";" + latLng.lng() });
                    }, 1000);
                });
            }, 2000)
        }



        private setAddressFromLatLng(latLng: google.maps.LatLng, input: HTMLInputElement) {
            var geocoder = new google.maps.Geocoder();

            geocoder.geocode({
                location: latLng,
                region: 'ru'
            }, (results, status) => {
                if(status == google.maps.GeocoderStatus.OK)
                    angular.element(input).val(results[0].formatted_address);


                angular.element(input).trigger("input");

                this.publicationsService.checkField(this.publicationIds, { fieldName: "address", fieldValue: input.value });
                this.publicationsService.checkField(this.publicationIds, { fieldName: "lat_lng", fieldValue: latLng.lat() + ";" + latLng.lng() });
            });
        }



        private initInputsChange() {
            angular.element("form[name='forms.publicationForm'] input, form[name='forms.publicationForm'] textarea").on("focusout", (e) => {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['value'].replace(/\s+/g, " ");

                if (!this.$scope.forms.publicationForm[name].$dirty) {
                    return;
                }

                this.publicationsService.checkField(this.publicationIds, { fieldName: name, fieldValue: value })
                    .success(response => {
                    if (response.data && !angular.element(e.currentTarget).is(":focus")) {
                        e.currentTarget['value'] = response.data.value ? response.data.value : value;
                    }

                    this.$scope.forms.publicationForm[name].$setValidity("invalid", true);
                })
                    .error(response => {
                    this.$scope.forms.publicationForm[name].$setValidity("invalid", response.code === 0);
                })
            });

            angular.element(".publication-view-container input[type='checkbox']").bind("change", function(e) {
                var name  = e.currentTarget['name'],
                    value = e.currentTarget['checked'];

                this.publicationsService.checkField(this.publicationIds, {
                    fieldName: name, fieldValue: value
                });
            });
        }



        private checkField(elementName) {
            var elementValue = null;

            this.validatePublicationOperation();

            if (elementName.indexOf('rent_') !== -1) {
                elementValue = this.$scope.publication.rent_terms[elementName.replace('rent_', '')];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });

            } else if (elementName.indexOf('sale_') !== -1) {
                elementValue = this.$scope.publication.sale_terms[elementName.replace('sale_', '')];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });

            } else if (!angular.isUndefined(this.$scope.publication.head[elementName])) {
                elementValue = this.$scope.publication.head[elementName];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });

            } else if (!angular.isUndefined(this.$scope.publication.body[elementName])) {
                elementValue = this.$scope.publication.body[elementName];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });

            } else if (!angular.isUndefined(this.$scope.publication.rent_terms[elementName])) {
                elementValue = this.$scope.publication.rent_terms[elementName];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });

            } else if (!angular.isUndefined(this.$scope.publication.sale_terms[elementName])) {
                elementValue = this.$scope.publication.sale_terms[elementName];
                this.publicationsService.checkField(this.publicationIds, { fieldName: elementName, fieldValue: elementValue });
            }
        }



        private validatePublicationOperation() {
            if (this.$scope.publication.head.for_sale == false && this.$scope.publication.head.for_rent == false) {
                this.$scope.publication.head.for_sale = true;
                this.checkField('for_sale');
            }
        }



        private scrollToBottom() {
            angular.element("main").animate({
                scrollTop: angular.element("main [ui-view]").height()
            }, "slow");
        }
    }
}