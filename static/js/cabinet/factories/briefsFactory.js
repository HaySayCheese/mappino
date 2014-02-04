'use strict';

app.factory('Briefs', function($rootScope, briefQueries) {
    var briefs = [];

    return {

        /**
         * @category {String, Number}
         * @callback {Function}
         **/
        load: function(category, callback) {
            var that = this;
            $rootScope.loadings.briefs = true;
            $rootScope.briefsLoaded = false;

            briefQueries.loadBriefs(category).success(function(data) {
                briefs = data;

                that.updateType();
                that.updateTags();

                $rootScope.loadings.briefs = false;
                $rootScope.briefsLoaded = true;

                callback(that.getAll());
            });
        },

        /**
         * @brief {Object}
         **/
        add: function(brief) {
            briefs.unshift(brief);
            this.updateType();
            this.updateTags();
        },

        getAll: function() {
            return briefs;
        },

        updateType: function() {
            var types = $rootScope.publicationTypes;

            for (var i = 0; i < briefs.length; i++) {
                for (var j = 0; j < types.length; j++) {
                    if (briefs[i].tid === types[j].id)
                        briefs[i].type = types[j].title;
                }
            }
        },

        updateTags: function() {
            var tags = $rootScope.tags;

            for (var i = 0; i < briefs.length; i++) {
                for (var j = 0; j < briefs[i].tags.length; j++) {
                    for (var k = 0; k < tags.length; k++) {
                        if (briefs[i].tags[j].id && (briefs[i].tags[j].id === tags[k].id))
                            briefs[i].tags[j] = tags[k];

                        if (!briefs[i].tags[j].id && (briefs[i].tags[j] === tags[k].id))
                            briefs[i].tags[j] = tags[k];

                        if ((briefs[i].tags[j].id && $rootScope.lastRemovedTag) && (briefs[i].tags[j].id === $rootScope.lastRemovedTag.id))
                            delete briefs[i].tags[j];
                    }
                }
            }
        },

        updateBriefOfPublication: function(tid, id, key, value) {
            for (var i = 0; i < briefs.length; i++) {
                if (briefs[i].tid == tid && briefs[i].id == id) {
                    briefs[i][key] = value;
                }
            }
        },

        isUnpublished: function(id) {
            var trues = false;
            for (var i = 0; i < briefs.length; i++) {
                if (briefs[i].id === parseInt(id) && briefs[i].title == "")
                    trues = true;
            }
            return trues;
        }
    }

});