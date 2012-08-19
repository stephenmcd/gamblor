
$(function() {

    var show = function(user) {
        var offset = $('.main').offset();
        var photo = MEDIA_URL + 'photos/' + user.id;
        $('.main').append('<div class="user" id="user-' + user.id + '">' +
                         '<img src="' + photo + '"></div>');
        $('#user-' + user.id).css({
            top: offset.top + user.y,
            left: offset.left + user.x,
        }).fadeIn();
    };

    socket.on('users', function(users) {
        $.map(users, show);
    });

    socket.on('join', function(user) {
        $('#user-' + user.id).remove();  // May still be fading out if reloaded
        show(user)
    });

    socket.on('leave', function(user) {
        $('#user-' + user.id).fadeOut(function() {
            $(this).remove();
        });
    });

});
