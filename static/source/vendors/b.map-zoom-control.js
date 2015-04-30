/**
 * Create a custom google map zoom control
 *
 * @param {Element}  div - Empty div
 * @param {google.maps.Map} map - Google Map object
 * @param {google.maps.ControlPosition} position - Google Map ControlPosition object
 */
function BMapZoomControl(div, map, position) {

    var container       = div;

    var zoomOut         = document.createElement('div');
    var zoomOutLabel    = document.createElement('div');

    var zoomIn          = document.createElement('div');
    var zoomInLabel     = document.createElement('div');



    container.index     = 1;
    container.className = 'zoom-control-buttons';



    // 'zoom in' container
    zoomIn.className = 'zoom-in-button';

    // 'zoom in' label (+)
    zoomInLabel.innerHTML = "<span class='glyphicon glyphicon-plus'></span>";



    // 'zoom out' container
    zoomOut.className = 'zoom-out-button';

    // 'zoom out' label (-)
    zoomOutLabel.innerHTML = "<span class='glyphicon glyphicon-minus'></span>";


    // append blocks
    zoomIn.appendChild(zoomInLabel);
    zoomOut.appendChild(zoomOutLabel);

    container.appendChild(zoomIn);
    container.appendChild(zoomOut);


    google.maps.event.addDomListener(zoomIn, 'click', function() {
        var zoom = map.getZoom();

        if(zoom !== 21) {
            map.setZoom(++zoom);
        }
    });

    google.maps.event.addDomListener(zoomOut, 'click', function() {
        var zoom = map.getZoom();

        if(zoom !== 0) {
            map.setZoom(--zoom);
        }
    });


    map.controls[google.maps.ControlPosition[position]].push(div);
}