$(function() {
    socket.on('roulette_landed_on', function(landed_on) {
        alert('Roulette landed on: ' + landed_on);
    });
});
