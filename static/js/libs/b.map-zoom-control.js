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


    var options = {
        container: {
            width:      '40px',
            height:     '80px',
            cursor:     'pointer',
            boxShadow:  '0 0 15px rgba(0, 0, 0, 0.4)',
            fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif"
        },
        zoomControl: {
            divider:                '1px solid #3281D7',
            transition:             "background-color 0.1s ease",
            backgroundColor:        '#318CE1',
            backgroundColorHover:   '#3286DC',
            label: {
                color:      '#ffffff',
                fontSize:   '28px'
            },
            zoomIn: {
                html: '<strong>+</strong>'
            },
            zoomOut: {
                html: '<strong>-</strong>'
            }
        }
    };


    // Set CSS for the controls
    container.index                     = 1;

    container.style.width               = options.container.width;
    container.style.height              = options.container.height;
    container.style.margin              = '10px 15px 10px 15px';
    container.style.cursor              = options.container.cursor;
    container.style.fontFamily          = options.container.fontFamily;
    container.style.boxShadow           = options.container.boxShadow;



    // 'zoom in' container
    zoomIn.style.display                = "block";
    zoomIn.style.height                 = '50%';
    zoomIn.style.backgroundColor        = options.zoomControl.backgroundColor;
    zoomIn.style.borderBottom           = options.zoomControl.divider;
    zoomIn.style.transition             = options.zoomControl.transition;
    zoomIn.style.webkitTransition       = options.zoomControl.transition;
    zoomIn.onmouseover                  = hoverHandler;
    zoomIn.onmouseout                   = hoverHandler;

    // 'zoom in' label (+)
    zoomInLabel.innerHTML               = options.zoomControl.zoomIn.html;
    zoomInLabel.style.fontSize          = options.zoomControl.label.fontSize;
    zoomInLabel.style.textAlign         = 'center';
    zoomInLabel.style.color             = options.zoomControl.label.color;
    zoomInLabel.style.msUserSelect      = "none";
    zoomInLabel.style.mozUserSelect     = "none";
    zoomInLabel.style.webkitUserSelect  = "none";



    // 'zoom out' container
    zoomOut.style.display               = "block";
    zoomOut.style.height                = '50%';
    zoomOut.style.backgroundColor       = options.zoomControl.backgroundColor;
    zoomOut.style.transition            = options.zoomControl.transition;
    zoomOut.style.webkitTransition      = options.zoomControl.transition;
    zoomOut.onmouseover                 = hoverHandler;
    zoomOut.onmouseout                  = hoverHandler;

    // 'zoom out' label (-)
    zoomOutLabel.innerHTML              = options.zoomControl.zoomOut.html;
    zoomOutLabel.style.fontSize         = options.zoomControl.label.fontSize;
    zoomOutLabel.style.textAlign        = 'center';
    zoomOutLabel.style.color            = options.zoomControl.label.color;
    zoomOutLabel.style.lineHeight       = "35px";
    zoomOutLabel.style.msUserSelect     = "none";
    zoomOutLabel.style.mozUserSelect    = "none";
    zoomOutLabel.style.webkitUserSelect = "none";


    // append blocks
    zoomIn.appendChild(zoomInLabel);
    zoomOut.appendChild(zoomOutLabel);

    container.appendChild(zoomIn);
    container.appendChild(zoomOut);



    /**
     * mouseover / mouseout handler to simulate hover state
     * on 'zoom in / zoom out' controls
     *
     * @param {Event} [e]
     **/
    function hoverHandler(e) {
        e.type === "mouseover" ?
            (this.style.backgroundColor = options.zoomControl.backgroundColorHover) :
                e.type === "mouseout" ?
                    (this.style.backgroundColor = options.zoomControl.backgroundColor) : '';
    }


    google.maps.event.addDomListener(zoomIn, 'click', function() {
        var zoom = map.getZoom();

        if(zoom != 21)
            map.setZoom(++zoom);
    });

    google.maps.event.addDomListener(zoomOut, 'click', function() {
        var zoom = map.getZoom();

        if(zoom != 0)
            map.setZoom(--zoom);
    });


    map.controls[google.maps.ControlPosition[position]].push(div);
}