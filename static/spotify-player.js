let player;
window.onSpotifyWebPlaybackSDKReady = () => {
    const token = access_token;
	player = new Spotify.Player({
        name: 'Q4-Team10-Capstone-Web-Player',
		getOAuthToken: cb => cb(token),
		volume: 1
	});
	player.addListener('ready', ({ device_id }) => {
		console.log('Ready with Device ID', device_id);
	});
    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });
    player.addListener('initialization_error', ({ message }) => {
        console.error('Failed to initialize', message);
    });
    player.addListener('authentication_error', ({ message }) => {
        console.error('Failed to authenticate', message);
    });
    player.addListener('account_error', ({ message }) => {
        console.error('Failed to validate Spotify account', message);
    });
    player.on('playback_error', ({ message }) => {
        console.error('Failed to perform playback', message);
    });
    document.getElementById('togglePlay').onclick = () => player.togglePlay();
    if (access_token.length > 1) {
        player.connect().then(success => {
            if (success) {
                // player.getCurrentState().then(state => {
                //     if (!state) {
                //         console.error('User is not playing music through the Web Playback SDK');
                //         return;
                //     }
                //     var current_track = state.track_window.current_track;
                //     var next_track = state.track_window.next_tracks[0];
                //     console.log(success, 'The Web Playback SDK successfully connected to Spotify!');
                //     console.log('Currently Playing', current_track);
                //     console.log('Playing Next', next_track);
                // })
            } else fetch('/refresh_token/').then(res => res.json()).then(location.reload)
        })
    }
    player.addListener('player_state_changed', state => {
        console.log(state)
        console.log('Currently Playing', state?.track_window.current_track.name);
        console.log('Position in Song', state?.position);
        console.log('Duration of Song', state?.duration);
    });
}