'use strict';

app.factory('Briefs', function($rootScope, briefQueries, Tags) {
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
            var that = this;
            $rootScope.loadings.briefs = true;

            briefQueries.searchInBriefs(value).success(function(data) {
                briefs = data;

                that.updateType();
                that.updateTags();

                $rootScope.loadings.briefs = false;

                typeof callback === 'function' && callback(that.getAll());
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

                if (_.isNumber(_.first(brief.tags))) {
                    _.each(brief.tags, function(id, index) {
                        brief.tags[index] = { id: id }
                    });
                }

                _.each(brief.tags, function(tag, index, list) {

                    if (tag.id === lastRemovedTagId) {
                        list.splice(index, 1);
                        return;
                    }

                    list[index] = _.first(_.where(tags, { id: tag.id }));
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

                if (brief.tid == tid && brief.id == id && key !== "tag") {
                    list[index][key] = value;
                    return;
                }

                if (brief.tid == tid && brief.id == id && key === "tag") {
                    var tag      = value.split(","),
                        tagId    = tag[0],
                        tagState = tag[1];

                    if (_.include(["true", true], tagState)) {
                        list[index].tags.push(Tags.getTagById(tagId));
                        publicationsCount[tagId] += 1;
                    } else {
                        list[index].tags.splice(list[index].tags.indexOf(Tags.getTagById(tagId)), 1);
                        publicationsCount[tagId] -= 1;
                    }
                }

            });
        }
    }

});