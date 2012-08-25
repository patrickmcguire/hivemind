var plotData = [];
var keys = [];

$("#zeitgesit-button").click(function() {
    plotData = [];
    keys = [];
    var terms = []
    
    for (i = 1; i <= 4; i++) {
        var val = $("#id_term" + i).val();
        if ("" !== val && undefined !== val && null !== val) {
            terms.push(val);
        }
    }
    
    $.each(terms, function(i,v) {
        $.ajax({
            url: "/bwog/" + v + "/",
            method: "GET",
            success: function(data) {
                keys.push(v);
                plotData.push(data);
            }
        });
    }
}

function replot() {
    var plot = $.jqplot('plot', plotData, {
        title: "Bwog phrase data"
    }
}
