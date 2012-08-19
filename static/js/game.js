
// Routines used across all games. See the js/games directory
// for game specific JS.

$(function() {

    /*socket.on('game_users', function(game, users) {
        var text = users.length > 0 ? 'Players: ' + users.join(', ') : '';
        $('.game-' + game + ' .players').html(text);
    });

    socket.on('game_end', function(game, results) {
        $('.game-' + game + ' .players').html('');
    });*/

    // Make the chips draggable.
    $('.chip').draggable({
        helper: 'clone',
        cursor: 'move',
        cursorAt: {top: 50},
    });

    // Make the game tables targets for dropping chips.
    $('.game').droppable({
        drop: function(event, ui) {
            var game = $(this);
            game.find('#id_amount').val(ui.draggable.text());
            game.find('form').submit();
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
            socket.emit('bet', game, amount, args);
            return false;
        });
    });

});
