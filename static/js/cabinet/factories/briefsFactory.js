'use strict';

app.factory('Briefs', function($rootScope, Queries, Tags) {
    var briefs = [],
        publicationTypes,
        publicationsCount = $rootScope.publicationsCount;

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

            Queries.Briefs.load(category, function(data) {
                briefs = data;

                that.updateType();
                that.updateTags();

                $rootScope.loadings.briefs = false;

                _.isFunction(callback) && callback(data);
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
        },


        /**
         * Пошук в брифах
         *
         * @param {string}      value       Строка пошука
         * @param {function}    callback    Вертає масив брифів
         */
        search: function(value, callback) {
            var that = this;
            $rootScope.loadings.briefs = true;

            Queries.Briefs.search(value, function(data) {
                briefs = data;

                that.updateType();
                that.updateTags();

                $rootScope.loadings.briefs = false;

                _.isFunction(callback) && callback(data);
            });
        },


        /**
         * Оновлює тип брифа з ідентифікатора типа
         */
        updateType: function() {
            publicationTypes = $rootScope.publicationTypes;

            _.each(briefs, function(brief) {
                brief.typeTitle = _.where(publicationTypes, { id: brief.tid })[0].title;
            });
        },


        /**
         * Оновлює теги брифа з масива тегів
         */
        updateTags: function() {
            var tags = Tags.getAll(),
                lastRemovedTag   = $rootScope.lastRemovedTag,
                lastRemovedTagId = lastRemovedTag ? lastRemovedTag.id : null;

            _.each(briefs, function(brief, index) {

                if (_.isNumber(_.first(brief.tags))) {              // Якщо елемент в масиві - число
                    _.each(brief.tags, function(id, index) {        // пробігаємось по них
                        brief.tags[index] = { id: id }              // і формуємо обєкти
                    });
                }

                _.each(brief.tags, function(tag, index, list) {

                    if (tag.id === lastRemovedTagId) {              // Якщо 'id' тега співпадає з останнім видаленим
                        list.splice(index, 1);                      // то видаляємо його з тегів брифа
                        return;                                     // ну і капут
                    }
                                                                          // Ну а якшо 'id' не співпадає з останнім видаленим
                    list[index] = _.first(_.where(tags, { id: tag.id })); // то оновлюємо теги брифа
                });
            });
        },


        /**
         * Оновлює параметр брифа
         *
         * @param {number} tid              Ідентифікатор типу оголошення
         * @param {number} id               Ідентифікатор оголошення
         * @param {string} key              Параметр який потрібно обновити
         * @param {string, number} value    Значення параметра який потрібно обновити
         */
        updateBriefOfPublication: function(tid, id, key, value) {

            if (!_.contains(["title", "for_sale", "for_rent", "tag"], key))
                return;

            _.each(briefs, function(brief, index, list) {

                if (brief.tid == tid && brief.id == id && key !== "tag") {          // Якщо 'tid' і 'id' спіпадають а ключ не 'tag'
                    list[index][key] = value;                                       // то оновлюємо параметр який передали в 'key'
                    return;                                                         // ну і капут
                }

                if (brief.tid == tid && brief.id == id && key === "tag") {          // А вот якщо ключ таки 'tag' то:
                    var tag      = value.split(","),                                // змінні...
                        tagId    = tag[0],
                        tagState = tag[1],
                        publicationsCount = $rootScope.publicationsCount;

                    if (_.include(["true", true], tagState)) {                      // якщо тег був доданий
                        list[index].tags.push(Tags.getTagById(tagId));              // то додаємо його в теги брифа

                        !publicationsCount[tagId]                                   // це оновлення лічильника в меню на сайті
                            ? (publicationsCount[tagId] = 0, publicationsCount[tagId] += 1)
                            : publicationsCount[tagId] +=1;
                    } else {                                                        // но якшо тег був видалений
                        list[index].tags.splice(list[index].tags.indexOf(Tags.getTagById(tagId)), 1); // видаляємо з тегів брифа

                        (!publicationsCount[tagId] || publicationsCount[tagId] < 0) // ну і о5 оновлюємо лічильник в меню на сайті
                            ? publicationsCount[tagId] = 0
                            : publicationsCount[tagId] -=1;
                    }
                }

            });
        },


        /**
         * Вертає масив брифів
         *
         * @return {Array} Масив брифік
         */
        getAll: function() {
            return briefs;
        }
    }

});