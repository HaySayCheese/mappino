app.filter('toHtml', function ($sce) {
    return function(text) {
        return $sce.trustAsHtml(text);
    }
});