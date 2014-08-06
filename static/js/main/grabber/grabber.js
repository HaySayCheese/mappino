/**
 * Created by sergei on 04.08.14.
 *
 * @license MIT
 */
var Grabber = {
    modalContentClass: ".publication-view-modal .modal-content",
    maxRepeatCount: 10,
    repeatInterval: 1000,

    init: function() {
        this.viewPage();
    },


    viewPage: function() {
        var self = this,
            urls = [];

        this.getUrls(function(data) {
            urls = data;
            console.log(urls);


            for (var i = 0; i < urls.length; i++) {
                var interval = null;
                window.location = "http://127.0.0.1:8000/#!/publication/" + urls[i] + "/";


                (function(_interval, urls, i) {
                    var repeatCount = 0;

                    _interval = setInterval(function () {
                        console.log(repeatCount);

                        if (repeatCount == self.maxRepeatCount) {
                            window.clearInterval(_interval);
                        }

                        if ($(self.modalContentClass).find(".publication-content-header span").text().length) {
                            self.parse(urls[i].split(":")[0], urls[i].split(":")[1], $("html"));

                            window.clearInterval(_interval);
                        }

                        repeatCount++;
                    }, self.repeatInterval);
                })(interval, urls, i);
            }
        });
    },


    parse: function(tid, hid, data) {
        var self = this;

        self.sendHtml(tid, hid, $(data).html())
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
                console.log("ok")
            }
        });
    },


    getUrls: function(callback) {
        var urls = [];

        $.ajax({
            type: "GET",
            url: "/ajax/api/grabber/iMvorMXScUgbbDGuJGCbnTnQwPRFKk/",
            success: function(data) {
                console.log(data);
                for (var i = 0; i < data.length; i++) {
                    urls.push(data[i][0] + ":" + data[i][1]);
                }

                callback(urls);
            }
        });
    }

};