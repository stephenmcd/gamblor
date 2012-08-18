
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
        var text = users.length > 0 ? 'Players: ' + users.join(', ') : '';
        $('.game-' + game + ' .players').html(text);
    });

    socket.on('game_end', function(game, results) {
        $('.game-' + game + ' .players').html('');
    });

    socket.emit('start');

    $('.game form').each(function(i, form) {
        $(form).submit(function() {
            var game, amount, args = [];
            $.each($(form).serializeArray(), function(i, field) {
                switch (field.name) {
                    case 'game':
                        game = field.value;
                        break;
                    case 'amount':
                        amount = field.value;
                        break;
                    default:
                        args[args.length] = field.value;
                }
            });
            socket.emit('bet', game, amount, args);
            return false;
        });
    });

});
