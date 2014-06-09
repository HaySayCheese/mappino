app.filter('newlines', function () {
    return function(text) {
        return text.replace(/\r\n/g, '<br/>');
    }
});