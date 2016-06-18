// JavaScript Document
$(document).ready(function () {
	check_login();
    //set what happens when the "Enter" button is pressed
    $('form#login-form').submit(function (event) {
        login(event);
    });
});

function check_login() {
	$.ajax("http://127.0.0.1:5000/rest_api/v1.0/already_signin",
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

    var json = {email: email, password: password};
        $.ajax("http://127.0.0.1:5000/rest_api/v1.0/signin",
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