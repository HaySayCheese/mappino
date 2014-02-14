'use strict';

app.factory('Publication', function($rootScope, publicationQueries, $location, lrNotifier, Briefs) {

    var publication = [],
        channel = lrNotifier('mainChannel');

    return {


        /**
         * Загружає оголошення
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        load: function(tid, id, callback) {
            var that = this;

            publicationQueries.loadPublication(tid, id).success(function(data) {
                publication = data;

                typeof callback === 'function' && callback(that.getAll());
            });
        },


        /**
         * Створення нового оголошення
         *
         * @param {object} publication Обєкт оголошення
         * @param {function} callback
         */
        create: function(publication, callback) {
            publicationQueries.createPublication(publication).success(function(data) {

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

                typeof callback === 'function' && callback(data);
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
            publicationQueries.publish(tid, id).success(function(data) {
                var briefs = Briefs.getAll();

                for (var i = 0; i < briefs.length; i++) {
                    if (briefs[i].id == id) {
                        $location.path("/publications/published/" + tid + ":" + id);
                        briefs.splice(i, 1);
                        break;
                    }
                }

                channel.info("Объявление успешно опубликовано");

                typeof callback === 'function' && callback(data);
            });
        },


        /**
         * Перенесення оголошення в чорновики
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        unpublish: function(tid, id, callback) {
            publicationQueries.unpublish(tid, id).success(function(data) {
                typeof callback === 'function' && callback(data);
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

            publicationQueries.checkInputs(tid, id, data).success(function(data) {

                if (inputName == "title" || inputName == "for_sale" || inputName == "for_rent" || inputName == "tag")
                    Briefs.updateBriefOfPublication(tid, id, inputName, data.value ? data.value : inputValue);

                typeof callback === 'function' && callback(data.value ? data.value : inputValue, data.code);
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
            publicationQueries.uploadPhotos(tid, hid, data).success(function(data) {
                typeof callback === 'function' && callback(data);
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
            publicationQueries.removePhoto(tid, hid, pid).success(function(data) {

                for (var i = 0; i < publication.photos.length; i++) {
                    if (publication.photos[i].id === pid) {
                        publication.photos.splice(i, 1);
                        break;
                    }
                }

                typeof callback === 'function' && callback(data);
            });
        },


        /**
         * Вертає масив з параметрами оголошення
         *
         * @return {Array}
         */
        getAll: function() {
            return publication;
        }

    }

});