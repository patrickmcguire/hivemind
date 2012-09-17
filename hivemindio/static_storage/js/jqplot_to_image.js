function jqplotToImg(objId) {
    // This is just copypasta from the Internet, discretion is advised
    // first we draw an image with all the chart components
    var newCanvas = document.createElement("canvas");
    newCanvas.width = $("#" + objId).width();
    newCanvas.height = $("#" + objId).height();
    var baseOffset = $("#" + objId).offset();

    $("#" + objId).children().each(function() {
        // // for the div's with the X and Y axis
        if ('div' == $(this)[0].tagName.toLowerCase()) {
            // X axis is built with canvas
            $(this).children("canvas").each(function() {
                var offset = $(this).offset();
                newCanvas.getContext("2d").drawImage(this, offset.left - baseOffset.left, offset.top - baseOffset.top);
            });
            // Y axis got div inside, so we get the text and draw it on
            // the canvas
            $(this).children("div").each(function() {
                var offset = $(this).offset();
                var context = newCanvas.getContext("2d");
                context.font = $(this).css('font-style') + " " + $(this).css('font-size') + " " + $(this).css('font-family');
                context.fillText($(this).html(), offset.left - baseOffset.left, offset.top - baseOffset.top + 10);
            });
        }
        // all other canvas from the chart
        else if ('canvas' == $(this)[0].tagName.toLowerCase()) {
            var offset = $(this).offset();
            newCanvas.getContext("2d").drawImage(this, offset.left - baseOffset.left, offset.top - baseOffset.top);
        }
    });

    // add the point labels
    $("#" + objId).children(".jqplot-point-label").each(function() {
        var offset = $(this).offset();
        var context = newCanvas.getContext("2d");
        context.font = $(this).css('font-style') + " " + $(this).css('font-size') + " " + $(this).css('font-family');
        context.fillText($(this).html(), offset.left - baseOffset.left, offset.top - baseOffset.top + 10);
    });

    // add the rectangles
    $("#" + objId + " *").children(".jqplot-table-legend-swatch").each(function() {
        var offset = $(this).offset();
        var context = newCanvas.getContext("2d");
        context.setFillColor($(this).css('background-color'));
        context.fillRect(offset.left - baseOffset.left, offset.top - baseOffset.top, 15, 15);
    });

    // add the legend
    $("#" + objId + " *").children(".jqplot-table-legend td:last-child").each(function() {
        var offset = $(this).offset();
        var context = newCanvas.getContext("2d");
        context.font = $(this).css('font-style') + " " + $(this).css('font-size') + " " + $(this).css('font-family');
        context.fillText($(this).html(), offset.left - baseOffset.left, offset.top - baseOffset.top + 15);
    });
    return newCanvas;
}

function newImage(objId) {
    newCanvas = jqplotToImage(objId);
    window.open(newCanvas.toDataURL(), "directories=no");
}


