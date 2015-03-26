app.factory('uuid', function() {
    return {
        new: function() {
            function _p8(s) {
                var p = (Math.random().toString(16) + "000000000").substr(2, 8);
                return s ? "-" + p.substr(0, 4) + "-" + p.substr(4, 4) : p;
            }
            return String.fromCharCode(65 + Math.floor(Math.random() * 26)) + _p8() + _p8(true) + _p8();
        }
    };
});