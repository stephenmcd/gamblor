$(function() {

    socket.on('craps_rolled', function(rolled, again) {
        again = again ? ' (rolling again)' : '';
        alert('Craps rolled: ' + rolled.join('/') + again);
    });

});
