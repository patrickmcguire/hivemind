function (terms) {
    var getarray = [], i, len;
    for (i = 0, len = data.length; i < len; i += 1) {
        getarray.push(getNote(data[i].key));
    };
    $.when.apply($, getarray).done(function () {
        
    });
}

$(document).ready(function() {
    plotData = [];
    keys = [];
    var terms = [];
    
    
})
