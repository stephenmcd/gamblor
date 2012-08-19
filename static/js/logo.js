
// Faux flashing casino-like logo - flickers it on and off randomly.

$(function() {

    var flicker = function() {
        var logo = $('.logo');
        var speed = 100;
        var times = Math.ceil(3 * Math.random());
        var once = function() {
            logo.fadeOut(speed, function() {
                logo.fadeIn(speed, function() {
                    if (times-- > 0) {
                        once();
                    }
                });
            });
        };
        once();
        setTimeout(flicker, 5000 + (10000 * Math.random()));
    };

    flicker();

});
