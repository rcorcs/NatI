var session_id = '{GroovesharkUnlocker-SessionId}';
var uuid = '{GroovesharkUnlocker-UUID}';

console.log('UNLOCKED by koehlma');
console.log('SessionID: ' + session_id);
console.log('UUID: ' + uuid);

console.log('Activate Crossfade Hack');
$('#player_crossfade').click(function (event) {
    event.stopPropagation();
    var crossfade_button = $('#player_crossfade');
    if (crossfade_button.hasClass('active')) {
        GS.player.setCrossfadeEnabled(false);
    } else {
        GS.player.setCrossfadeEnabled(true);
    }
});
