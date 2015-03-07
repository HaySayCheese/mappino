function BMapZoomControl(div, map) {

    var container = div;
    var zoomOut = document.createElement('div');
    var zoomOutText = document.createElement('div');

    var zoomIn = document.createElement('div');
    var zoomInText = document.createElement('div');



    // Set CSS for the controls.
    container.style.width               = '40px';
    container.style.height              = '81px';
    container.style.margin              = '0 0 10px 15px';
    container.style.cursor              = 'pointer';
    container.style.fontFamily          = "'Helvetica Neue', Helvetica, Arial, sans-serif";
    container.style.backgroundColor     = "#3175CB";
    container.style.boxShadow           = '0 0 15px rgba(0, 0, 0, 0.4)';



    zoomIn.style.display                = "block";
    zoomIn.style.width                  = '100%';
    zoomIn.style.height                 = '50%';
    zoomIn.style.marginBottom           = '1px';
    zoomIn.style.backgroundColor        = "#318CE1";
    container.appendChild(zoomIn);

    zoomInText.innerHTML                = '<strong>+</strong>';
    zoomInText.style.fontSize           = '28px';
    zoomInText.style.textAlign          = 'center';
    zoomInText.style.color              = "#ffffff";
    zoomIn.appendChild(zoomInText);



    zoomOut.style.display               = "block";
    zoomOut.style.width                 = '100%';
    zoomOut.style.height                = '50%';
    zoomOut.style.backgroundColor       = "#318CE1";
    container.appendChild(zoomOut);

    zoomOutText.innerHTML               = '<strong>-</strong>';
    zoomOutText.style.fontSize          = '28px';
    zoomOutText.style.textAlign         = 'center';
    zoomOutText.style.color             = "#ffffff";
    zoomOutText.style.marginBottom      = "5px";
    zoomOutText.style.lineHeight        = "35px";
    zoomOut.appendChild(zoomOutText);



    // Setup the click event listeners for zoom-in, zoom-out:
    google.maps.event.addDomListener(zoomOut, 'click', function() {
        var currentZoomLevel = map.getZoom();

        if(currentZoomLevel != 0)
            map.setZoom(currentZoomLevel - 1);
    });

    google.maps.event.addDomListener(zoomIn, 'click', function() {
        var currentZoomLevel = map.getZoom();

        if(currentZoomLevel != 21)
            map.setZoom(currentZoomLevel + 1);
    });
}