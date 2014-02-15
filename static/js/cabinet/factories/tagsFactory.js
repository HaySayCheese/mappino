'use strict';

app.factory('Tags', function($rootScope, lrNotifier, tagQueries) {
    var tags = [],
        tagParameters = {
            colors:         ["#9861dd", "#465eec", "#60b4cf", "#54b198", "#7cc768", "#dfb833", "#f38a23", "#f32363"],

            defaultTagName: "Название",
            title:          "Название",

            defaultColor:   "#9861dd",
            selectedColor:  "#9861dd"
        },
        channel = lrNotifier('mainChannel');

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
                _.each(data.dirtags, function(tag, index) {
                    that.add({
                        id: tag.id,
                        title: tag.title,
                        color_id: tag.color_id,
                        color: tagParameters.colors[tag.color_id]
                    });
                });

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

                if (data.code !== 0) {
                    channel.warn("Тег с таким именем уже существует");
                    typeof callback === 'function' && callback("error");
                    return;
                }

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
         * @param {object}   updatedTag Обєкт тега
         * @param {function} callback
         */
        update: function(updatedTag, callback) {
            tagQueries.editTag(updatedTag).success(function(data) {

                if (data.code !== 0) {
                    channel.warn("Тег с таким именем уже существует");
                    typeof callback === 'function' && callback("error");
                    return;
                }

                _.each(tags, function(tag, index, list) {
                    if (tag.id === updatedTag.id)
                        list[index] = updatedTag;
                });

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


        /**
         * Вертає тег по ідентифікатору
         *
         * @param {number} id Ідентифікатор тега
         * @return {object}   Обєкт тега
         */
        getTagById: function(id) {
            return _.first(_.filter(tags, function(tag) {
                return tag.id == id;
            }));
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