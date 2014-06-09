app.filter('newlines', function ($compile) {
    return function(text) {
        return text.replace(/\r\n/g, '<br/>');
    }
});