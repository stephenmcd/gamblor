$(function() {

    // Number was landed on - simulate spin.
    socket.on('roulette_landed_on', function(landed_on) {
        var message = $('.message-roulette');
        message.text('No more bets!');
        var rotate = 10000 + Math.random() * 360;
        var start = {rotate: '0deg'};
        var stop = {rotate: rotate + 'deg'};
        $('.wheel').transition(start).transition(stop, 5000, 'snap');
        // Wait for spin to finish, display number landed on,
        // then revert message back to waiting for bets.
        setTimeout(function() {
            message.text('Landed on ' + landed_on + '!');
            setTimeout(function() {
                message.text('Place your bets!');
            }, 5000);
        }, 5000);
    });

    // Set the number the chip was dropped on in the betting form.
    gameHandlers.roulette = function(form, number) {
        $(form).find('[name="number"]').val($(number).text());
    };

});
