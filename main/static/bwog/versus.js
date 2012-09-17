$(document).ready(function() {
    $('#versus-submit').on('click', function() {
        var term1 = $('#term1').text();
        var term2 = $('#term2').text();
        $.ajax({
            url: '/bwog/correlation',
            data: {
                term1: term1,
                term2: term2,
            },
            accepts: 'application/json',
            success: function(data) {
                $('#versus-table').children('.num_comments');
            },
        });
    });

});
