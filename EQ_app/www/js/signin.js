// JavaScript Document
$(document).ready(function () {
	check_login();
    //set what happens when the "Enter" button is pressed
    $('form#login-form').submit(function (event) {
        login(event);
    });
});

function check_login() {
	$.ajax("http://192.168.1.102:8080/rest_api/v1.0/already_signin",
            {
                method: 'GET',

                contentType: 'application/json',

                success: function (data, status) {
                   	window.location.assign("map.html");
                }
            }
        );
}

function login(event) {
    var email = $("input[name='email']").val();
    var password = $("input[name='password']").val();
	var patient = $("input[name='patient']").val();
	var anorapp = ''; var deviceid = '';
	if (userAgent.match( /Android/i )) anorapp = 'android';
	else anorapp = 'ios';
	
	var push = PushNotification.init({ "android": {"senderID": "836442599686"},
         "ios": {"alert": "true", "badge": "true", "sound": "true"}});

    push.on('registration', function(data) {
       	deviceid = data.registrationId;
    });
	
	push.on('notification', function(data) {
		cordova.plugins.notification.local.schedule({
    		title: "New history notification",
    		text: data.message,
    		sound: "default",
    		icon: "/images/logoStanford32.png"
		});

		cordova.plugins.notification.local.on("click", function (notification) {
    		window.location.assign('history.html');
		});
	});

	push.on('error', function(e) {
		console.log(e.message);
	});

    var json = {patient: patient, email: email, password: password, deviceid:deviceid, anorapp:anorapp};
        $.ajax("http://192.168.1.102:8080/rest_api/v1.0/signin",
            {
                method: 'POST',

                contentType: 'application/json',
                data: JSON.stringify(json),
				
				statusCode: {
					404: function() {
						alert('This account probably doesn\'t exist.');		
					},
					403: function() {
						alert('You have may inserted the wrong password.');
					},
				},

                success: function (data, status) {
                    window.location.assign('map.html');
                },
            }
        );

   //avoid form submission (the default action of the event)
   event.preventDefault();
}