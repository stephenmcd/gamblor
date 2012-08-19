
// Sets up the socket.io connection.

$(function() {

    socket = io.connect(':' + SOCKETIO_PORT, {
        transports: ['websocket', 'htmlfile', 'xhr-multipart',
                     'xhr-polling', 'jsonp-polling']
    });
    socket.emit('start');

    /*socket.on('notice', function(notice) {
        alert(notice);
    });
    */

})
