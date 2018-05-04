var socket = io.connect('http://' + document.domain + ':' + location.port);

var sioRoomId;

socket.on('connect', function() {
	socket.emit('initConnection', {data: socket.id});
})

function sendSocketIOChatMsg(msg) {
	socket.emit('chat msg send', {"sioRoom": sioRoomId, "message": msg});
}

function sendNewRequest() {
	var reqClass = $('#newRequestClass').find(':selected').text();
	var reqTopic = $('#newRequestTopic').val();
	var reqLoc = $('#newRequestLocation').find(':selected').text();
	var reqDesc = $('#newRequestDescription').val();
	var newRequestData = {"class": reqClass, "topic": reqTopic, "loc": reqLoc, "desc": reqDesc};
	socket.emit('listing new', newRequestData);
	$('#chatWindow').show();
	// DISABLE NEW REQUEST BUTTON
}

socket.on('listing broadcast', function(msg) {
	var alert = `
<div class="alert alert-success" role="alert" id="listing`+msg.lid+`">
	<div id="uid" hidden="true">`+msg.uid+`</div>
	<strong>` + msg.class + `</strong> ` + msg.desc + 
	` <button type="button" class="btn btn-success pull-right" onclick="acceptRequest(` + msg.lid + `)"><span class="glyphicon glyphicon-ok"></span></button>
	<button type="button" class="btn btn-danger pull-right" onclick="dismissRequest(` + msg.lid + `)"><span class="glyphicon glyphicon-remove"></span></button>
</div>`;
	$('#listingsTable').append(alert);
	console.log(msg);
});

socket.on('chat msg init', function(msg) {
	sioRoomId = msg.roomid;
	console.log(sioRoomId);
});

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
		</div>
	</div>
</div>`;
	$('#chatBoxMessages').append(recvMsgHTML);
}