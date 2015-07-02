'use strict';

app.factory('Publication', function($rootScope, Queries, $location, lrNotifier, Briefs) {

    var publication = [],
        publicationChartData = [],
        channel = lrNotifier('mainChannel'),
        publicationsCount = $rootScope.publicationsCount,

        publicationTypes = $rootScope.publicationTypes = [
            { name: "flat",      id: 0,  title: "Квартиры" },
            { name: "house",     id: 1,  title: "Дома" },
            { name: "room",      id: 2,  title: "Комнаты" },
            { name: "land",      id: 3,  title: "Земельного участка" },
            { name: "garage",    id: 4,  title: "Гаража" },
            { name: "office",    id: 5,  title: "Офиса" },
            { name: "trade",     id: 6,  title: "Торгового помещения" },
            { name: "warehouse", id: 7,  title: "Склада" },
            { name: "business",  id: 8,  title: "Готового бизнеса" }
        ];

    return {


        /**
         * Загружає дані оголошення
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        load: function(tid, id, callback) {
            var that = this;

            Queries.Publications.load(tid, id, function(data) {
                publication = data;

                that.setDefaults();

                _.isFunction(callback) && callback(that.getAll());
            });
        },


        /**
         * Загружає дані графіків для опублікованого оголошення
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        loadChartData: function(tid, id, callback) {
            var that = this,
                days = 0,
                resolution = window.innerWidth;

            resolution <= 1024 ? days = 7 :
                resolution >= 1024 && resolution <= 1600 ? days = 14 :
                    days = 30;

            Queries.Publications.loadChartData(tid, id, days, function(data) {
                publicationChartData = [];

                _.each(data, function(col, index, list) {
                    publicationChartData.push({
                        "c": [
                            {
                                "v": new Date(new Date(col.date).setHours(0, 0, 0, 0))
                            }, {
                                "v": col.views
                            }, {
                                "v": col.contacts_requests
                            }
                        ]
                    });
                });

                _.isFunction(callback) && callback(publicationChartData);
            });
        },


        /**
         * Створення нового оголошення
         *
         * @param {object} publication Обєкт з полями оголошення
         * @param {function} callback
         */
        create: function(publication, callback) {
            publication.tid = parseInt(publication.tid);
            publicationsCount = $rootScope.publicationsCount;

            Queries.Publications.create(publication, function(data) {

                if ($rootScope.routeSection === "unpublished")
                    Briefs.add({
                        id: data.id,
                        for_rent: publication.for_rent,
                        for_sale: publication.for_sale,
                        photo_url: "",
                        tags: [],
                        title: "",
                        tid: publication.tid
                    });

                publicationsCount['all']         += 1;
                publicationsCount['unpublished'] += 1;

                $rootScope.$emit('publicationCreated');

                $location.path("/publications/unpublished/" + publication.tid + ":" + data.id);

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Публікація оголошення
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        publish: function(tid, id, callback) {
            Queries.Publications.publish(tid, id).success(function(data) {

                if (data.code !== 0) {
                    channel.info("При публикации произошла ошибка, попробуйте еще раз");
                    _.isFunction(callback) && callback(data);
                    return;
                }

                var briefs = Briefs.getAll();

                _.each(briefs, function(brief, index, list) {
                    if (brief.id == id) {
                        $location.path("/publications/published/" + tid + ":" + id);
                        list.splice(index, 1);
                    }
                });


                publicationsCount['unpublished'] -= 1;
                publicationsCount['published']   += 1;

                channel.info("Объявление успешно опубликовано");

                _.isFunction(callback) && callback(data);
            }).error(function(data) {
                channel.info("При публикации произошла ошибка, попробуйте еще раз");
                _.isFunction(callback) && callback(data);
            })
        },


        /**
         * Перенесення оголошення з опублікованих в неопубліковані
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        unpublish: function(tid, id, callback) {
            Queries.Publications.unpublish(tid, id, function(data) {

                publicationsCount['published']      -= 1;
                publicationsCount['unpublished']    += 1;

                $location.path("publications/unpublished/" + tid + ":" + id);

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Перенесення оголошення в корзину
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        toTrash: function(tid, id, callback) {
            Queries.Publications.toTrash(tid, id, function(data) {
                switch (publication.head.state_sid) {
                    case 0:
                        publicationsCount['published'] -= 1;
                        break;
                    case 1:
                        publicationsCount['unpublished'] -= 1;
                        break;
                    case 2:
                        publicationsCount['trash'] -= 1;
                        break;
                }

                publicationsCount['all']   -= 1;
                publicationsCount['trash'] += 1;

                $location.path("publications/" + $rootScope.routeSection);

                channel.info("Объявление перемещено в корзину");

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Видалення оголошення
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        remove: function(tid, id, callback) {
            Queries.Publications.remove(tid, id, function(data) {
                publicationsCount['trash'] -= 1;

                _.each(publication.tags ? publication.tags : publication.head.tags, function(tag, index, list) {
                    publicationsCount[index] -= 1;
                });

                $location.path("/publications/trash");
                channel.info("Объявление успешно удалено");

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Перенесення з корзини в неопубліковані
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        toUnpublished: function(tid, id, callback) {
            Queries.Publications.unpublish(tid, id, function(data) {

                publicationsCount['trash']       -= 1;
                publicationsCount['unpublished'] += 1;
                publicationsCount['all']         += 1;

                $location.path("publications/unpublished/" + tid + ":" + id);

                channel.info("Объявление восстановлено в неопубликованные");

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Відправка полів вводу на сервер для перевірки
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {object} data             Обєкт з іменем поля вводу та його значенням
         * @param {function} callback
         */
        checkInputs: function(tid, id, data, callback) {
            var inputName   = data.f,
                inputValue  = data.v;

            Queries.Publications.check(tid, id, data, function(data) {

                if (_.contains(["title", "for_sale", "for_rent", "tag"], inputName))
                    Briefs.updateBriefOfPublication(tid, id, inputName, data.value ? data.value : inputValue);

                _.isFunction(callback) && callback(data.value ? data.value : inputValue, data.code);
            });
        },


        /**
         * Загрузка фотографій
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} hid              Ідентифікатор оголошення
         * @param {object} data             Обєкт з іменем поля вводу та його значенням
         * @param {function} callback
         */
        uploadPhotos: function(tid, hid, data, callback) {
            Queries.Publications.uploadPhotos(tid, hid, data, function(data) {

                if (data.code === 100) {
                    channel.info("Во время загрузки возникла ошибка. Повторите попытку с другим изображением");
                    _.isFunction(callback) && callback(data);
                    return;
                }

                publication.photos.push(data.image);

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Видалення фотографії
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} hid              Ідентифікатор оголошення
         * @param {object} pid              Ідентифікатор фотографії
         * @param {function} callback
         */
        removePhoto: function(tid, hid, pid, callback) {
            Queries.Publications.removePhoto(tid, hid, pid, function(data) {

                _.each(publication.photos, function(photo, index, list) {
                    if (photo.id === pid) {
                        if (photo.is_title)
                            Briefs.updateBriefOfPublication(tid, hid, "photo_url", "");

                        list.splice(index, 1);
                    }
                });

                _.each(publication.photos, function(photo, index, list) {
                    if (photo.id == data.photo_id) {
                        list[index].is_title = true;

                        Briefs.updateBriefOfPublication(tid, hid, "photo_url", data.brief_url);
                    }
                });

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Видалення фотографії
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} hid              Ідентифікатор оголошення
         * @param {object} pid              Ідентифікатор фотографії
         * @param {function} callback
         */
        setMainPhoto: function(tid, hid, pid, callback) {
            Queries.Publications.setMainPhoto(tid, hid, pid, function(data) {

                _.each(publication.photos, function(photo, index, list) {

                    photo.is_title = false;

                    if (pid === photo.id) {
                        list[index].is_title = true;

                        Briefs.updateBriefOfPublication(tid, hid, "photo_url", data.brief_url);
                    }
                });

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Вертає масив з параметрами оголошення
         *
         * @return {Array}
         */
        getAll: function() {
            return publication;
        },


        /**
         * Вертає кількість оголошень в кожному розділі
         */
        getCounts: function() {
            Queries.Publications.counts(function(data) {
                publicationsCount = $rootScope.publicationsCount = data;
            });
        },


        /**
         * Вертає масив з типами оголошення
         *
         * @return {Array}
         */
        getTypes: function() {
            return publicationTypes;
        },


        /**
         * Встановлення базових значень для полів
         */
        setDefaults: function() {
            if (_.isNull(publication.sale_terms)) {
                publication.sale_terms = {};

                _.defaults(publication.sale_terms, {
                    add_terms:      "",
                    currency_sid:   0,
                    is_contract:    false,
                    price:          null,
                    sale_type_sid:  0,
                    transaction_sid: 0
                });
            }

            if (_.isNull(publication.rent_terms)) {
                publication.rent_terms = {};

                _.defaults(publication.rent_terms, {
                    add_terms:      "",
                    currency_sid:   0,
                    is_contract:    false,
                    period_sid:     1,
                    persons_count:  null,
                    price:          null,
                    rent_type_sid:  0
                });
            }
        }

    }

});