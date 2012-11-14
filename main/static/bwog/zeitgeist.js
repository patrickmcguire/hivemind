var plotData = [];
var keys = [];
var plot;

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
                replot();
            }
        });
    });
});

function replot() {
    $('#plot').html('');
    plot = $.jqplot('plot', plotData, {
        title: "Bwog phrase data",
        axes: {
            xaxis: {
                renderer: $.jqplot.DateAxisRenderer,
                tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                tickOptions: {
                    formatString: '%b %y',
                    angle: '45'
                }
            },
            yaxis: {
                min: 0
            }
        },
        series: zipKeys(),
        highlighter: {
            show: true,
            sizeAdjust: 7.5
        },
        legend: { 
            show: true, 
            placement: 'outsideGrid'
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

function zipKeys() {
    var zipped = [];
    if (2 === keys.length) {
        zipped = [
            {label: keys[0], color: '#27719D'},
            {label: keys[1], color: '#259F61'},
        ];
    } else {
        $.each(keys, function(i,v) {
            zipped.push({label: v});
        });
    }
    return zipped;
}
