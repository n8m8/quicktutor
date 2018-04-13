// when a tutor receives a tutor request from another user
socket.on('tut req recv', function(data) {
	// get user ID for chat protocol
	var duid = data.userId;
	duid = -1;
	// CODE TO DISPLAY DIV
	// DIV SHOULD AUTO DESTROY AFTER 15/30 MINS
	tutorRequestConfirm(duid);
});

function tutorRequestConfirm(uid) {
	// when this gets received on backend, need to get suid from app.py
	socket.emit('tut req confirm', {duid: uid, classId: -1});
}

socket.on('user tut recv', function(data) {
	// get tutor user ID for chat protocol
	var duid = data.userId;
	var requestid = data.reqId;
	duid = requestid = -1;
	userTutorConfirm(duid);
});

function userTutorConfirm(uid, reqid) {
	socket.emit('user tut confirm', {duid: uid, requestid: reqid})
}