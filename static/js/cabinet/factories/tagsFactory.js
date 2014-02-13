'use strict';

app.factory('Tags', function($rootScope, tagQueries) {
    var tags = [],
        tagParameters = {
            colors:         ["#9861dd", "#465eec", "#60b4cf", "#54b198", "#7cc768", "#dfb833", "#f38a23", "#f32363"],

            defaultTagName: "Название",
            title:          "Название",

            defaultColor:   "#9861dd",
            selectedColor:  "#9861dd"
        };

    return {


        /**
         * Завантаження тегів
         *
         * @param {function} callback
         */
        load: function(callback) {
            var that = this;
            $rootScope.loadings.tags = true;

            tagQueries.loadTags().success(function(data) {
                for (var i = 0; i <= data.dirtags.length - 1; i++) {
                    tags.push({
                        id: data.dirtags[i].id,
                        title: data.dirtags[i].title,
                        color_id: data.dirtags[i].color_id,
                        color:tagParameters.colors[data.dirtags[i].color_id]
                    });
                }

                $rootScope.loadings.tags = false;
                $rootScope.$broadcast('tagsUpdated');

                callback(that.getAll());
            });
        },


        /**
         * Додання тега
         *
         * @param {object} tag Обєкт тега
         */
        add: function(tag) {
            tags.push(tag);

            $rootScope.$broadcast('tagsUpdated');
        },


        /**
         * Створення тега
         *
         * @param {object} tag Обєкт тега
         * @param {function} callback
         */
        create: function(tag, callback) {
            var that = this;
            tagQueries.createTag(tag).success(function(data) {

                if (data.code === 1)
                    return;

                that.add({
                    id: data.id,
                    title: tag.title,
                    color: tag.selectedColor,
                    color_id: tag.colors.indexOf(tag.selectedColor)
                });

                $rootScope.$broadcast('tagsUpdated');

                typeof callback === 'function' && callback();
            });
        },


        /**
         * Онолвення значень тега
         *
         * @param {object} tag          Обєкт тега
         * @param {function} callback
         */
        update: function(tag, callback) {
            tagQueries.editTag(tag).success(function() {
                for (var i = 0; i <= tags.length - 1; i++)
                    if (tags[i].id == tag.id) {
                        tags[i] = tag;
                        break;
                    }

                $rootScope.$broadcast('tagsUpdated');

                typeof callback === 'function' && callback();
            });
        },


        /**
         * Видалення тега
         *
         * @param {object} tag Обєкт тега
         */
        remove: function(tag) {
            tagQueries.removeTag(tag.id).success(function() {
                tags.splice(tags.indexOf(tag), 1);
                $rootScope.lastRemovedTag = tag;

                $rootScope.$broadcast('tagsUpdated');
            });
        },


        getTagById: function(id) {
            var returnedTag = {};

            for (var i = 0; i < tags.length; i++) {
                if (tags[i].id === parseInt(id)) {
                    returnedTag = tags[i];
                    break;
                }
            }

            return returnedTag;
        },


        /**
         * Повернення обєкта з тегами
         *
         * @return {Array} Вертає масив тегів
         */
        getAll: function() {
            return tags;
        },


        /**
         * Повернення обєкта з базовими параметрами тега
         *
         * @return {object} Вертає обєкт з параметрами
         */
        getParameters: function() {
            return tagParameters;
        }

    }
});