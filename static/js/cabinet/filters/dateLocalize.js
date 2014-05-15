"use strict";

app.filter('dateLocalize', function () {
    return function (utcDate) {
        var date = new Date(utcDate),
            millis = date.getTime();

        date.setTime(millis + (date.getTimezoneOffset() * -1) * 60 * 1000);
        console.log(utcDate)
        console.log(date)
        return date;
    }
});