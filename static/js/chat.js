
// Handles chat messages.

$(function() {

    // Just send the message to the socket.
    $('.chat').submit(function() {
        var input = $('.chat .message');
        socket.emit('chat', input.val());
        input.val('');
        input.focus();
        return false;
    });

    var chatTimeouts = {};

    socket.on('chat', function(user, message) {
        say(user.id, message);
    });

    // New message received - show it in a bootstrap tooltip on the
    // avatar of the user who sent it.
    say = function(uid, message) {
        // Their previous message may be closing the tooltip.
        clearTimeout(chatTimeouts[uid]);
        var avatar = $('#user-' + uid);
        // Hack that lets us set a new value each time.
        avatar.attr('data-original-title', message);
        avatar.tooltip('show');
        chatTimeouts[uid] = setTimeout(function() {
            closeChat(avatar);
        }, 5000);
    }

    // Just closes the tooltip. Also called from users.js when a user
    // moves, since the tooltip can't follow them.
    closeChat = function(avatar) {
        avatar.attr('data-original-title', '');
        avatar.tooltip('hide');
    };

});
