'use strict';

app.factory('Publication', function($rootScope, publicationQueries, $location, lrNotifier, Briefs) {

    var publication = [],
        channel = lrNotifier('mainChannel'),

        publicationTypes = $rootScope.publicationTypes = [
            { name: "house",     id: 0,  title: "Дома" },
            { name: "flat",      id: 1,  title: "Квартиры" },
            { name: "apartments",id: 2,  title: "Аппартаментов" },
            { name: "dacha",     id: 3,  title: "Дачи" },
            { name: "cottage",   id: 4,  title: "Коттеджа" },
            { name: "room",      id: 5,  title: "Комнаты" },
            { name: "trade",     id: 6,  title: "Торгового помещения" },
            { name: "office",    id: 7,  title: "Офиса" },
            { name: "warehouse", id: 8,  title: "Склада" },
            { name: "business",  id: 9,  title: "Готового бизнеса" },
            { name: "catering",  id: 10, title: "Обьекта общепита" },
            { name: "garage",    id: 11, title: "Гаража" },
            { name: "land",      id: 12, title: "Земельного участка" }
        ];

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

                _.each(briefs, function(brief, index, list) {
                    if (brief.id == id) {
                        $location.path("/publications/published/" + tid + ":" + id);
                        list.splice(index, 1);
                    }
                });

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

                if (!_.contains(["title", "for_sale", "for_rent", "tag"], inputName))
                    return;

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

                _.each(publication.photos, function(photo, index, list) {
                    if (photo.id === pid)
                        list.splice(index, 1);
                });

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
        },


        /**
         * Вертає масив з типами оголошення
         *
         * @return {Array}
         */
        getTypes: function() {
            return publicationTypes;
        }

    }

});