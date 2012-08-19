$(function() {

    socket.on('craps_rolled', function(rolled, again) {
        var message = $('.message-craps');
        var text = 'Rolled ' + rolled.join(' and ');
        if (again) {
            text += ', rolling again';
        }
        message.text(text);
    });

});
