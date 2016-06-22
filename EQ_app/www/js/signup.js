// JavaScript Document
$(document).ready(function () {
    //set what happens when the "Enter" button is pressed
    $('form#signup-form').submit(function (event) {
        signup(event);
    });
});

function signup(event) {
	var name = $("input[name='name']").val();
	var surname = $("input[name='surname']").val();
    var email = $("input[name='email']").val();
    var password = $("input[name='password']").val();
	var password2 = $("input[name='password2']").val();
	var bcod = $("input[name='bcod']").val();

    var json = {name: name, surname: surname, email: email, password: password, bcod: bcod};
	if(password!==password2) {
		alert('The two passwords don\'t match.')	;
		event.preventDefault();
	} else if (password.length < 8) {
        alert('Password must be at least of 8 characters!');
        event.preventDefault();
    } else {	
    	$.ajax("http://192.168.1.102:8080/rest_api/v1.0/signup",
        	{
            	method: 'POST',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
				statusCode: {
					405: function() {
						alert('The inserted code or the e-mail are already registered into this system.');
					},
					404: function() {
						alert('This bracelet has not been sold yet.');
					},
					403: function() {
						alert('Impossible to process signup request.');	
					}
				},
            	success: function (data, status) {
                    window.location.assign('login.html');
					alert('A new account has been created, you can log in now.');
                }
        	 }
    	);
	}
    //avoid form submission (the default action of the event)
    event.preventDefault();
}