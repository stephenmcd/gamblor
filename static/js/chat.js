$(function() {

    $('.chat').submit(function() {
        var input = $('.chat .message');
        socket.emit('chat', input.val());
        input.val('');
        input.focus();
        return false;
    });

    var chatTimeouts = {};

    socket.on('chat', function(user, message) {
        clearTimeout(chatTimeouts[user.id]);
        var avatar = $('#user-' + user.id);
        avatar.attr('data-original-title', message);
        avatar.tooltip('show');
        chatTimeouts[user.id] = setTimeout(function() {
            closeChat(avatar);
        }, 5000);
    });

    closeChat = function(avatar) {
        avatar.attr('data-original-title', '');
        avatar.tooltip('hide');
    };

});
