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

                callback(that.getTags());
            });
        },

        add: function(tag) {
            tags.push(tag);
        },

        update: function(tag, callback) {
            tagQueries.editTag(tag).success(function() {
                for (var i = 0; i <= tags.length - 1; i++)
                    if (tags[i].id == tag.id)
                        tags[i] = tag;

                callback();
            });
        },

        remove: function(tag) {
            tagQueries.removeTag(tag.id).success(function() {
                tags.splice(tags.indexOf(tag), 1);
                $rootScope.lastRemovedTag = tag;
            });
        },

        getTags: function() {
            return tags;
        },

        getParameters: function() {
            return tagParameters;
        }

    }
});