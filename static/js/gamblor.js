
$(function() {

    var socket = io.connect(':9000', {
        transports: ['websocket', 'htmlfile', 'xhr-multipart',
                     'xhr-polling', 'jsonp-polling']
    });

    socket.on('users', function(users) {
        console.log('users: ', users);
    });

    socket.on('join', function(user) {
        console.log('joined: ', user);
    });

    socket.on('leave', function(user) {
        console.log('left: ', user);
    });

    socket.emit('start');

});
