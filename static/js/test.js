$(function() {

    $('#command').focus();

    $('#send_get').click(function() {
        $.get($('#command').val() + '?' + $('#argument').val(), function(data) {
            $('#response').html(JSON.stringify(data, undefined, 2));
        }, 'json');
    });

    $('#send_post').click(function() {
        $.post($('#command').val(), $('#argument').val(), function(data) {
            $('#response').html(JSON.stringify(data, undefined, 2));
        }, 'json');
    });

});
