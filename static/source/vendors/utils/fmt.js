/**
 * "{0} is dead, but {1} is alive! {0} {2}".format("ASP", "ASP.NET")
 **/

if (!String.prototype.fmt) {
    String.prototype.fmt = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}