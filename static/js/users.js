
// Manages user avatars and their movement.

$(function() {

    var zIndex = 1;  // Incremented and applied to avatars each time they move.
    var MOVE_PX = 3;  // How many pixels our own avatar moves per interval
    var MOVE_INTERVAL_MS = 10;  // How many milliseconds for each interval
    var move;  // Stores the interval handler so we can clear it
    var dir;  // Stores the top/left amount of pixels to move.

    // Handles showing an avatar, both when a new user joins other users,
    // and when we join and we need to show all current users.
    var show = function(user) {
        var offset = $('.main').offset();
        var photo = MEDIA_URL + 'photos/' + user.id;
        var body = STATIC_URL + 'img/body.png';
        $('.main').append('<div class="user" id="user-' + user.id + '">' +
                          '<img class="photo" src="' + photo + '"><br>' +
                          '<img class="body" src="' + body + '""></div>');
        $('#user-' + user.id).css({
            zIndex: zIndex++,
            top: offset.top + user.y,
            left: offset.left + user.x,
        }).fadeIn();
    };

    // Initial user list when we join.
    socket.on('users', function(users) {
        $.map(users, show);
    });

    // Someone else has joined.
    socket.on('join', function(user) {
        $('#user-' + user.id).remove();  // May still be fading out if they reloaded
        show(user)
    });

    // Remove a user when they leave.
    socket.on('leave', function(user) {
        $('#user-' + user.id).fadeOut(function() {
            $(this).remove();
        });
    });

    // On arrow keypress, move the avatar.
    $(document).keydown(function(e) {

        var avatar = $('#user-' + userID);

        // Might not have rendered ourselves yet.
        if (avatar.length == 0) {
            return;
        }

        // Map arrow keys to pixels.
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
                // Ensure we're not outside the main area.
                outside = avatar.collision('.main', {mode: 'protrusion'}).length
                // Ensure we're not on one of the game tables.
                // TODO: extend collision detection to other avatars.
                collided = avatar.collision('.game').length;
                if (outside || collided) {
                    avatar.css(pos);
                }
            }, MOVE_INTERVAL_MS);
        }

    });

    // On arrow keyup, send our new position to the server, which
    // will broadcast it to everyone else so they can update our
    // position on their screen.
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

    // Handle other avatars movemebts being broadcast.
    socket.on('move', function(user) {
        var avatar = $('#user-' + user.id);
        closeChat(avatar);
        var offset = $('.main').offset();
        var to = {
            top: offset.top + user.y,
            left: offset.left + user.x
        };
        var offset = avatar.offset();
        // Simulate the amount of time the movement would take
        // using the same logic we move our own avatar with.
        var distance = Math.max(Math.abs(to.top - offset.top),
                                Math.abs(to.left - offset.left));
        var duration = distance / MOVE_PX * MOVE_INTERVAL_MS;
        avatar.css({zIndex: zIndex++}).animate(to, duration, 'linear');
    });

});
