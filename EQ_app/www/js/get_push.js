// JavaScript Document
document.addEventListener("deviceready",onDeviceReady,false);
function onDeviceReady() {
	var push = PushNotification.init({ "android": {"senderID": "836442599686"},
         "ios": {"alert": "true", "badge": "true", "sound": "true"}, "windows": {} } );

	push.on('notification', function(data) {

	});

	push.on('error', function(e) {
		console.log(e.message);
	});
}