/**
 * Файл з загальними змінними
 **/

angular.module('mappino.pages.map').value('TXT', {
    'SERVICE_NAME': 'Mappino'
});

angular.module('mappino.pages.map').value('LoadedValues', {
    'sidebar': {
        'templates': {
            'red':      false,
            'blue':     false,
            'green':    false,
            'yellow':   false
        }
    },

    'filters': {
        'parsed': false
    },

    'map': {
        'loaded': false
    }
});