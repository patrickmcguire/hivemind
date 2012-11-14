$(document).ready(function() {
    $('#versus-submit').on('click', function() {
        var term1 = $('#inputTerm1').attr('value');
        var term2 = $('#inputTerm2').attr('value');
        $.ajax({
            url: '/bwog/correlation/',
            data: {
                term1: term1,
                term2: term2,
            },
            contentType: 'application/json',
            success: function(data) {
                var num_comments = $('#versus-table').children('.num_comments');
            },
        });
    });
});
