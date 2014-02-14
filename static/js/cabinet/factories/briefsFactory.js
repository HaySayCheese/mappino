'use strict';

app.factory('Briefs', function($rootScope, briefQueries, Tags) {
    var briefs = [];

    return {

        /**
         * Загружає брифи оголошень
         *
         * @param {string, number}  category    Категорія ('all', 'published', 'unpublished', ...)
         * @param {function}        callback    Вертає масив брифів при успішній загрузці
         */
        load: function(category, callback) {
            var that = this;
            $rootScope.loadings.briefs = true;

            briefQueries.loadBriefs(category).success(function(data) {
                briefs = data;

                that.updateType();
                that.updateTags();

                $rootScope.loadings.briefs = false;

                typeof callback === 'function' && callback(that.getAll());
            });
        },


        /**
         * Додає бриф
         *
         * @param {object} brief Обєкт брифа
         */
        add: function(brief) {
            briefs.unshift(brief);

            this.updateType();
            this.updateTags();
        },


        /**
         * Вертає масив брифів
         *
         * @return {Array} Масив брифік
         */
        getAll: function() {
            return briefs;
        },


        /**
         * Пошук в брифах
         *
         * @param {string}      value       Строка пошука
         * @param {function}    callback    Вертає масив брифів
         */
        search: function(value, callback) {
            briefQueries.searchInBriefs(value).success(function(data) {
                typeof callback === 'function' && callback(data);
            });
        },


        /**
         * Оновлює тип брифа з ідентифікатора типа
         */
        updateType: function() {
            var types = $rootScope.publicationTypes;

            for (var i = 0; i < briefs.length; i++) {
                for (var j = 0; j < types.length; j++) {
                    if (briefs[i].tid === types[j].id) {
                        briefs[i].type = types[j].title;
                    }
                }
            }
        },


        /**
         * Оновлює теги брифа з масива тегів
         */
        updateTags: function() {
            var tags = Tags.getAll();

            for (var i = 0; i < briefs.length; i++) {
                for (var j = 0; j < briefs[i].tags.length; j++) {

                    if (!tags.length) {
                        briefs[i].tags = [];
                        return;
                    }

                    for (var k = 0; k < tags.length; k++) {

                        if ((briefs[i].tags[j].id && $rootScope.lastRemovedTag) && (briefs[i].tags[j].id === $rootScope.lastRemovedTag.id)) {
                            briefs[i].tags.splice(briefs[i].tags.indexOf($rootScope.lastRemovedTag), 1);
                            return;
                        }

                        if (briefs[i].tags[j].id && (briefs[i].tags[j].id === tags[k].id)) {
                            briefs[i].tags[j] = tags[k];
                        }


                        if (!briefs[i].tags[j].id && (briefs[i].tags[j] === tags[k].id)) {
                            briefs[i].tags[j] = tags[k];
                        }
                    }
                }
            }
        },


        /**
         * Оновлює параметр брифа
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {object} key              Параметр який потрібно обновити
         * @param {string, number} value    Значення параметра який потрібно обновити
         */
        updateBriefOfPublication: function(tid, id, key, value) {

            for (var i = 0; i < briefs.length; i++) {
                if (briefs[i].tid == tid && briefs[i].id == id && key == "tag") {
                    var tag = value.split(","),
                        tagId = tag[0],
                        tagState = tag[1];

                    if (tagState === "true" || tagState === true) {
                        briefs[i].tags.push(Tags.getTagById(tagId));
                        return;
                    }


                    if (tagState === "false" || tagState === false) {
                        briefs[i].tags.splice(briefs[i].tags.indexOf(Tags.getTagById(tagId)), 1);
                        return;
                    }

                    return;
                }

                if (briefs[i].tid == tid && briefs[i].id == id) {
                    briefs[i][key] = value;
                    return;
                }
            }
        }
    }

});