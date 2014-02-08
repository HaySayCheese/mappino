'use strict';

app.factory('Publication', function($rootScope, publicationQueries, Briefs) {

    var publication = [];

    return {


        /**
         * Загружає оголошення
         *
         * @param {string} category         Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        load: function(category, tid, id, callback) {
            var that = this;

            publicationQueries.loadPublication(category, tid, id).success(function(data) {
                publication = data;

                callback(that.getAll());
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
                        tags: "",
                        title: "",
                        tid: publication.tid
                    });

                callback(data);
            });
        },


        /**
         * Публікація оголошення
         *
         * @param {string} category         Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        publish: function(category, tid, id, callback) {
            publicationQueries.publish(category, tid, id).success(function(data) {
                callback(data);
            });
        },


        /**
         * Перенесення оголошення в чорновики
         *
         * @param {string} category         Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {function} callback
         */
        unpublish: function(category, tid, id, callback) {
            publicationQueries.unpublish(category, tid, id).success(function(data) {
                callback(data);
            });
        },


        /**
         * Відправка полів вводу на сервер для перевірки
         *
         * @param {string} category         Категорія ('all', 'published', 'unpublished', ...)
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {object} data             Обєкт з іменем поля вводу та його значенням
         * @param {function} callback
         */
        checkInputs: function(category, tid, id, data, callback) {
            var inputName   = data.f,
                inputValue  = data.v;

            publicationQueries.checkInputs(category, tid, id, data).success(function(data) {

                if (data.value)
                    callback(data.value);

                if (inputName == "title" || inputName == "for_sale" || inputName == "for_rent")
                    Briefs.updateBriefOfPublication(tid, id, inputName, data.value ? data.value : inputValue);
            });
        },


        uploadPhotos: function(tid, hid, data, callback) {
            publicationQueries.uploadPhotos(tid, hid, data).success(function(data) {
                callback(data);
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