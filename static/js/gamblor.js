
$(function() {

    socket = io.connect(':9000', {
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

    socket.on('notice', function(notice) {
        alert(notice);
    });

    socket.on('game_users', function(game, users) {
        console.log('users for game ', game, users);
    });

    socket.on('game_end', function(game, users) {
        console.log('game ended ', game, users);
    });

    socket.emit('start');

});
