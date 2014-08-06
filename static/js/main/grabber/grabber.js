/**
 * Created by sergei on 04.08.14.
 *
 * @license MIT
 */
var Grabber = {
    modalContentClass: ".publication-view-modal .modal-content",
    modalContentLoaderClass: ".publication-loading",

    init: function() {
        this.getUrls();
    },


    viewPage: function(urls, i) {
        var self = this;

        window.location = "http://127.0.0.1:8000/#!/publication/" + urls[i] + "/";

        var tid = urls[i].split(":")[0],
            hid = urls[i].split(":")[1];


        self.tryGetHtml(tid, hid, function() {
            i++;

            if (i == urls.length)
                return;

            self.viewPage(urls, i);
        });
    },


    tryGetHtml: function(tid, hid, callback) {
        var self = this;

        setTimeout(function() {
            if (self.contentIsLoading()) {
                self.sendHtml(tid, hid, $("html").html());

                callback();
            } else {
                self.tryGetHtml(tid, hid);
            }
        }, 2000);
    },

    contentIsLoading: function() {
        var self = this;

        return $(self.modalContentClass).find(self.modalContentLoaderClass).hasClass("ng-hide");
    },


    sendHtml: function(tid, hid, data) {
        $.ajax({
            type: "POST",
            url: "/ajax/api/grabber/iMvorMXScUgbbDGuJGCbnTnQwPRFKk/",
            data: {
                tid: tid,
                hash_id: hid,
                html: data
            },
            success: function(data) {
                console.info(tid + ":" + hid + " - parsed!");
            }
        });
    },


    getUrls: function() {
        var self = this,
            urls = [];

        $.ajax({
            type: "GET",
            url: "/ajax/api/grabber/iMvorMXScUgbbDGuJGCbnTnQwPRFKk/",
            success: function(data) {
                console.log("Received " + data.length + " urls.");

                for (var i = 0; i < data.length; i++) {
                    urls.push(data[i][0] + ":" + data[i][1]);
                }

                if (!urls.length) {
                    console.info("All urls parsed!");
                    return;
                }

                self.viewPage(urls, 0);
            }
        });
    }

};