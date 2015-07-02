'use strict';

app.factory('Tags', function($rootScope, lrNotifier, Queries) {
    var tags = [],
        tagParameters = {
            colors:         ["#9861dd", "#465eec", "#60b4cf", "#54b198", "#7cc768", "#dfb833", "#f38a23", "#f32363"],
            default_title: "Название",
            default_color:   "#9861dd"
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
            $rootScope.loadings.tags = true;                    // Оновлюємо індикатор загрузки

            Queries.Tags.load(function(data) {                  // Грузим теги
                _.each(data.dirtags, function(tag) {            // Пробігаємся по всіх шо притянули
                    that.add(tag);                              // і додаємо їх за допомогою функції 'add'
                });

                $rootScope.loadings.tags = false;               // Оновлюємо індикатор загрузки
                $rootScope.$emit('tagsUpdated');                // Кажемо всім шо в нас є теги

                _.isFunction(callback) && callback(data.dirtags); // Вертаєм колбек з тим шо притянули
            });
        },


        /**
         * Додання тега
         *
         * @param {object} tag Обєкт тега
         */
        add: function(tag) {
            if (!tag.id && !arguments[1].id)                // Якщо в тега нема 'id' і його не передають в 'arguments[1]'
                return;                                     // то капут

            if (arguments[1] && arguments[1].id)            // Но якщо все таке в 'arguments[1]' є id'
                tag.id = arguments[1].id;                   // то приміняємо його до тега

            tag.color = tagParameters.colors[tag.color_id]; // Оновлюємо колір в тега з 'tagParameters.colors' по його 'id'

            tags.push(tag);                                 // І нарешті додаємо тег в масив тегів 'tags'

            $rootScope.$emit('tagsUpdated');                // І на кінець кажемо всім шо в нас новий тег
        },


        /**
         * Створення нового тега
         *
         * @param {object} tag Обєкт тега
         * @param {function} callback
         */
        create: function(tag, callback) {
            var that = this;

            if (!tag.color_id)                                                  // Якщо в тега нема 'color_id'
                tag.color_id = tagParameters.colors.indexOf(tag.selected_color); // ставим його з 'tagParameters.colors' по його вибраному кольору

            Queries.Tags.create({ title: tag.title, color_id: tag.color_id } , function(data) {

                if (data.code !== 0) {                                          // Якщо 'data.code' не '0'
                    _.isFunction(callback) && callback("error");                // вертаєм колбек шо біда
                    return;                                                     // ну і капут
                }

                that.add(tag, { id: data.id });                                 // Но якшо таки все ок то додаємо тег
                $rootScope.publicationsCount[data.id] = 0;                      // Ставимо лічильник в 0

                $rootScope.$emit('tagsUpdated');                                // Кажем всім шо в нас новий тег

                _.isFunction(callback) && callback(tags);                       // І вертаємо колбек з тегами
            });
        },


        /**
         * Онолвення значень тега
         *
         * @param {object}   updatedTag Обєкт тега
         * @param {function} callback
         */
        update: function(updatedTag, callback) {
            Queries.Tags.update(updatedTag.id, { title: updatedTag.title, color_id: updatedTag.color_id }, function(data) {

                if (data.code !== 0) {                                  // Якщо 'data.code' не '0'
                    channel.warn("Тег с таким именем уже существует");  // кричимо шо біда
                    _.isFunction(callback) && callback("error");        // вертаємо колбек шо біда
                    return;                                             // ну і капут
                }

                _.each(tags, function(tag, index, list) {               // Якшо не капут то пробуємо оновити дані тега
                    if (tag.id === updatedTag.id)                       // Якшо находимо
                        list[index] = updatedTag;                       // то оновлюємо тег
                });

                $rootScope.$emit('tagsUpdated');                        // Кажем всім шо в нас новий тег

                _.isFunction(callback) && callback(tags);               // І вертаємо колбек з тегами
            });
        },


        /**
         * Видалення тега
         *
         * @param {object} tag Обєкт тега
         * @param {function} callback
         */
        remove: function(tag, callback) {
            Queries.Tags.remove(tag.id ,function(data) {
                tags.splice(tags.indexOf(tag), 1);          // Якшо все ок то видаляємо тег

                $rootScope.lastRemovedTag = tag;            // Зберігаємо останній видалений шо б видлити його з брифів

                $rootScope.$emit('tagsUpdated');            // Кажем всім шо в нас одного не стало
                channel.info("Ярлык '" + tag.title + "' успешно удален");

                _.isFunction(callback) && callback(tags);   // І вертаємо колбек з тегами
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