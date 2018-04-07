var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
	socket.emit('initConnection', {data: socket.id});
})

function sendSocketIOChatMsg(msg) {
	socket.emit('chat msg send', {message: msg});
}

socket.on('chat msg recv', function(msg) {
	console.log('Received: ' + msg.data);
	recvMsg(msg.data);
});

function recvMsg(message) {
	var recvMsgHTML = `
<div class="row msgContainer chatRecv">
	<div class="col-md-2 col-xs-2 name">
		<!-- MAYBE PROFILE PIC? -->
	</div>
	<div class="col-md-10 col-xs-10">
		<div class="message msgSend">
			<p id="msg">` + message + `</p>
			<p id="username">RECV</p>
		</div>
	</div>
</div>`;
	$('#chatBoxMessages').append(recvMsgHTML);
}