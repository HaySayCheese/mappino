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
            urls = this.getUrls();

        for (var i = 0; i <= urls.length - 1; i++) {
            var interval = null;
            window.location = urls[i];


            (function(_interval) {
                var repeatCount = 9;

                _interval = setInterval(function () {
                    console.log(repeatCount);

                    if (repeatCount == self.maxRepeatCount) {
                        window.clearInterval(_interval);
                    }

                    if ($(self.modalContentClass).length) {
                        self.parse($("body"));

                        window.clearInterval(_interval);
                    }

                    repeatCount++;
                }, self.repeatInterval);
            })(interval);
        }
    },


    parse: function(data) {
        console.log($(data).find(this.modalContentClass))
    },


    getUrls: function() {
        return [
            'http://mappino.com.ua/#!/publication/0:bc047e4cd3ce466391e95f0e4e79cc98'
        ]
    }

};