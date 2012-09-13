var plotData = [];
var keys = [];

$(document).ready(function() {
    plotData = [];
    keys = [];
    var terms = [];
    
    for (i = 1; i <= 4; i++) {
        var val = $("#id_term" + i).val();
        if ("" !== val && undefined !== val && null !== val) {
            terms.push(val);
        }
    }
    
    $.each(terms, function(i,v) {
        $.ajax({
            url: "/bwog/trend/" + v + "/",
            method: "GET",
            success: function(data) {
                keys.push(v);
                plotData.push(data);
                my_replot();
            }
        });
    });
});

function my_replot() {
    dataFill();
    max = null;
    var plot = $.jqplot('plot', plotData, {
        title: "Bwog phrase data",
        axes: {
            xaxis: {
                renderer: $.jqplot.DateAxisRenderer,
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    formatString: '%m %D',
                    angle: '90'
                }
            },
            yaxis: {
                min: 0
            }
        }
    });
}

// find out where some have data and others don't, put zeros in
function dataFill() {
    var hashes = [];
    var allKeys = {}
    $.each(plotData, function(k,v) {
        var hash = {};
        $.each(v, function(i, tuple) {
            hash[tuple[0]] = tuple[1];
            allKeys[tuple[0]] = true
        });
        hashes.push(hash);
    });

    var zeroFilled = []
    $.each(hashes, function(i, hash) {
        for (var key in allKeys) {
            key = parseInt(key);  //fuck your sneaky conversions
            if (!hash[key]) {
                hash[key] = 0;
            }
        }
        zeroFilled.push(hash)
    });
    
    $.each(zeroFilled, function(i, hash) {
        var newArray = [];
        $.each(hash, function(k, v) {
            var k = parseInt(k);
            newArray.push([k, v]);
        });
        newArray.sort(function(a,b) { a[0] - b[0]});
        plotData[i] = newArray;
    });
}
