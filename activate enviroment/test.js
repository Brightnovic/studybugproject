var webSocket;
var localStream = new MediaStream();
var messageList = document.querySelector('#message-list');

document.addEventListener('DOMContentLoaded', function () {
    var labelUsername = document.querySelector('#label-username');
    var usernameInput = document.querySelector('#username');
    var participantsDiv = document.getElementById('participants');
    var btnJoin = document.querySelector('#btn-join');
    var localVideo = document.querySelector('#local-video');
    var btnToggleAudio = document.querySelector('#btn-toggle-audio');
    var btnToggleVideo = document.querySelector('#btn-toggle-video');
    var mapPeers = {};

    function addLocalTracks(peer) {
        localStream.getTracks().forEach(track => {
            peer.addTrack(track, localStream);
        });
    }

    function addParticipant(username) {
        var participantElement = document.createElement('p');
        participantElement.textContent = username;
        participantsDiv.appendChild(participantElement);
    }

    function webSocketOnMessage(event) {
        var parsedData = JSON.parse(event.data);
        var peerUsername = parsedData['peer'];
        var action = parsedData['action'];

        if (username == peerUsername) {
            return;
        }

        var receiver_channel_name = parsedData['message']['receiver_channel_name'];

        if (action == 'new-peer') {
            createOfferer(peerUsername, receiver_channel_name);

            return;
        }


        if (action == 'new-offer') {
            var offer = parsedData['message']['sdp'];
            createAnswerer(offer, peerUsername, receiver_channel_name);
            return;
        }

        if (action == 'new-message') {
            var answer = parsedData['message']['sdp'];


            var peer = mapPeers[peerUsername][0];
            peer.setRemoteDescription(answer);
            return;
        }
    }

    btnJoin.addEventListener('click', () => {
        var username = usernameInput.value;
        addParticipant(username);

        if (username === "") {
            return;
        }
        
    var constraints = {
        'video': true,
        'audio': true
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            // User media acquisition
        })
        .catch(error => {
            console.log("Error getting user media:", error);
        });

    function createOfferer(peerUsername, receiver_channel_name) {
        // Function definition for createOfferer
    }

    function createAnswerer(offer, peerUsername, receiver_channel_name) {
        // Function definition for createAnswerer
    }

    function dcOnMessage(event) {
        // Function definition for dcOnMessage
    }

    function sendSignal(action, message) {
        // Function definition for sendSignal
    }

    function createVideo(peerUsername) {
        // Function definition for createVideo
    }

    function setOnTrack(peer, remoteVideo) {
        // Function definition for setOnTrack
    }

    function removeVideo(video) {
        // Function definition for removeVideo
    }
});
