
// Routines used across all games. See the js/games directory
// for game specific JS, which adds named handlers to the handlers
// object here.

var gameHandlers = {};

$(function() {

    socket.on('game_users', function(game, users) {
        $('.message-' + game).html('Current players: ' + users.length);
    });

    socket.on('game_end', function(game, results) {
        setTimeout(function() {
            $.each(results, function(uid, amount) {
                var message = amount > 0 ? 'I won $' + amount + '!' : 'I lost :(';
                say(uid, message);
            });
        }, 5000);
    });

    // Make the chips draggable.
    $('.chip').draggable({
        helper: 'clone',
        cursor: 'move',
        cursorAt: {top: 50},
        opacity: .6
    });

    // Make the game tables targets for dropping chips.
    $('.chip-drop').droppable({
        hoverClass: 'chip-drop-over',
        drop: function(event, ui) {
            var game = $(this);
            while (!game.hasClass('game')) {
                game = $(game.parent());
            }
            var form = game.find('form');
            var name = game.find('[name="game"]').val();
            if (gameHandlers[name]) {
                gameHandlers[name](form, this);
            }
            game.find('#id_amount').val(ui.draggable.text());
            form.submit();
        }
    });

    // Handles submitting the bet form for a game - builds up the
    // arguments and sends it to the socket.
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
            var balance = parseFloat($('.balance').text().replace('$', ''));
            balance -= amount;
            if (balance > 0) {
                $('.balance').text('$' + balance);
            }
            socket.emit('bet', game, amount, args);
            return false;
        });
    });

});
