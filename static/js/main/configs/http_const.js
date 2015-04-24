/**
 * Файл з константами для http запитів
 **/


app.constant('HTTP_URL', (function () {
    'use strict';

    return {
        'MAP': {
            'GET_MARKERS':                  '/ajax/api/markers/?p={0}'
        }
    };
})());