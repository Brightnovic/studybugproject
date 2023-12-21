var webSocket;
console.log("loaded main.js")
document.addEventListener('DOMContentLoaded', function () {
    var labelUsername = document.querySelector('#label-username');
    var usernameInput = document.querySelector('#username');
    var participantsDiv = document.getElementById('participants');
    var btnJoin = document.querySelector('#btn-join');
    var webSocket;
    var mapPeers = {};


    function addLocalTracks(peer) {
        localStream.getTracks().forEach(track => {
            peer.addTrack(track, localStream)
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

        // Hide the input field and disable the button after joining
        usernameInput.disabled = true;
        usernameInput.style.visibility = 'hidden';
        btnJoin.disabled = true;
        btnJoin.style.visibility = 'hidden';

        labelUsername.innerHTML = username;

        var loc = window.location;
        var wsStart = 'ws://';

        if (loc.protocol === 'https:') {
            wsStart = 'wss://';
        }

        var endPoint = wsStart + loc.host + loc.pathname;
        console.log('endpoint:', endPoint);

        webSocket = new WebSocket(endPoint);

        webSocket.addEventListener('open', (e) => {
            console.log("Connection opened!");
            sendSignal('new-peer', {})
        });

        webSocket.addEventListener('message', webSocketOnMessage);

        webSocket.addEventListener('close', (e) => {
            console.log("Connection closed!");
        });

        webSocket.addEventListener('error', (e) => {
            console.log(" an Error occurred!");
        });
    });
});


var localStream = new MediaStream();
const constraints = {
    'video': true,
    'audio': true
}
const localVideo = document.querySelector('#local-video');



const btnToggleAudio = document.querySelector('#btn-toggle-audio');
const btnToggleVideo = document.querySelector('#btn-toggle-video');


var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        
        localVideo.srcObject = localStream;
        localVideo.muted = true;

        var audioTracks = stream.getAudioTracks();
        var videoTracks = stream.getVideoTracks();


        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;


        btnToggleAudio.addEventListener('click', () => {
            audioTracks[0].enabled = !audioTracks[0].enabled;
            if (audioTracks[0].enabled) {
                btnToggleAudio.innerHTML = 'Audio Mute';
                return;
            }  
            btnToggleAudio.innerHTML = 'Audio Muted';
        })


        btnToggleVideo.addEventListener('click', () => {
            videoTracks[0].enabled = !videoTracks[0].enabled;
            if (videoTracks[0].enabled) {
                btnToggleVideo.innerHTML = 'video off';
                return;
            }  
            btnToggleVideo.innerHTML = 'video on';
        })

    }).catch(error => {
    console.log("Error getting user media:", error)
})
var messageList = document.querySelector('#message-list');

function createOfferer(peerUsername, receiver_channel_name) {
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var dc = peer.createDataChannel('channel');
    dc.addEventListener('open', () => {
        console.log("connection opened!");
    });
    dc.addEventListener('message', dcOnMessage);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);
    mapPeers[peerUsername] = [peer, dc];

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceconnectionstatechange = peer.iceConnectionState;
        if (iceconnectionstatechange === 'failed' || iceconnectionstatechange === 'disconnected' || iceconnectionstatechange === 'closed') {
            delete mapPeers[peerUsername];
            if (iceconnectionstatechange != 'closed') {
                peer.close();
            }
            remoteVideo(remoteVideo)
        }
        
    });
    peer.addEventListener('icecandidate', (event) => {
        if (event.candidate) {
            console.log('new ice candidate:', JSON.stringify(peer.localDescription));
            return;
        }

        sendSignal('new-profile', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });

    });

    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(() => {
            console.log('local description set successfully');
        });
}
///trying!
var audioTracks = stream.getAudioTracks();
audioTracks.forEach(track => {
    track.enabled = true; // Ensure the track is enabled
});

function createAnswerer(offer,peerUsername,receiver_channel_name) {
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);

    peer.addEventListener('datachannel', e => {
        peer.dc = e.channel;
        peer.dc.addEventListener('open', () => {
            console.log("connection opened!");
        });
        peer.dc.addEventListener('message', dcOnMessage);
        mapPeers[peerUsername] = [peer, peer.dc];
    });

   

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceconnectionstatechange = peer.iceConnectionState;
        if (iceconnectionstatechange === 'failed' || iceconnectionstatechange === 'disconnected' || iceconnectionstatechange === 'closed') {
            delete mapPeers[peerUsername];
            if (iceconnectionstatechange != 'closed') {
                peer.close();
            }
            remoteVideo(remoteVideo)
        }
        
    });
    peer.addEventListener('icecandidate', (event) => {
        if (event.candidate) {
            console.log('new ice candidate:', JSON.stringify(peer.localDescription));
            return;
        }

        sendSignal('new-answer', {
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });

    });

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log("remote description set successfully for %s", peerUsername);
           return peer.createAnswer();
        })
        .then(a => {
            console.log("answer created!");
            peer.setLocalDescription(a);
        })
}

function dcOnMessage(event) {
    var message = event.data;

    var li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    messageList.appendChild(li);
    
}

function sendSignal(action, message) {
    var JsonStr = JSON.stringify({
        'peer': username,
        'action': action,  
        'message':  message
    })
   

    // trying 
    webSocket.addEventListener('open', (e) => {
        console.log("Connection opened!");
        sendSignal('new-peer', {})
    });
    webSocket.send(JsonStr);
}

function createVideo(peerUsername) {
    
    var videoContainer = document.querySelector('#video-container');
    var remoteVideo = document.createElement('video');
    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    var videoWrapper = document.createElement('div');
    videoContainer.appendChild(videoWrapper);
    videoWrapper.appendChild(remoteVideo);
}

function setOnTrack(peer, remoteVideo) {
    var remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;


    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    });
}

function removeVideo(video) {
    var videoWrapper = video.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper)
}