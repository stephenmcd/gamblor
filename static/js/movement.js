
$(function() {

    var MOVE_PX = 3;
    var MOVE_INTERVAL_MS = 10;
    var move, dir;

    $(document).keydown(function(e) {

        var avatar = $('#user-' + userID);

        if (avatar.length == 0) {
            return;
        }

        dir = {
            37: {left: '-=' + MOVE_PX},
            38: {top:  '-=' + MOVE_PX},
            39: {left: '+=' + MOVE_PX},
            40: {top:  '+=' + MOVE_PX}
        }[e.keyCode];

        if (!move && dir) {
            closeChat(avatar);
            move = setInterval(function() {
                var pos = {
                    top: avatar.css('top'),
                    left: avatar.css('left')
                }
                dir.zIndex = zIndex++;
                avatar.css(dir);
                outside = avatar.collision('.main', {mode: 'protrusion'}).length
                collided = avatar.collision('.game').length;
                if (outside || collided) {
                    avatar.css(pos);
                }
            }, MOVE_INTERVAL_MS);
        }

    });

    $(document).keyup(function() {
        if (dir) { //  Only if valid keydown occurred.
            var offset = $('.main').offset();
            var avatar = $('#user-' + userID).offset();
            if (offset && avatar) {  // Might not have loaded yet.
                socket.emit('move', {
                    y: avatar.top - offset.top,
                    x: avatar.left - offset.left
                });
                clearInterval(move);
                move = null;
            }
        }
    });

    socket.on('move', function(user) {
        var avatar = $('#user-' + user.id);
        closeChat(avatar);
        var offset = $('.main').offset();
        var to = {
            top: offset.top + user.y,
            left: offset.left + user.x
        };
        var offset = avatar.offset();
        var distance = Math.max(Math.abs(to.top - offset.top),
                                Math.abs(to.left - offset.left));
        var duration = distance / MOVE_PX * MOVE_INTERVAL_MS;
        avatar.css({zIndex: zIndex++}).animate(to, duration, 'linear');
    });

});
