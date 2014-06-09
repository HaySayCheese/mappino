app.filter('newlines', function ($sce) {
    return function(text) {
        return $sce.trustAsHtml(text.replace(/\r\n/g, '<br/>'));
    }
});