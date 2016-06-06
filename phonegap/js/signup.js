// JavaScript Document
// JavaScript Document
$(document).ready(function () {
    //set what happens when the "Enter" button is pressed
    $('form#submit-form').submit(function (event) {
        signup(event);
    });
});

function signup(event) {
	var name = $("input[name='name']").val();
	var surname = $("input[name='surname']").val();
    var email = $("input[name='mail']").val();
    var password = $("input[name='password']").val();
	var password2 = $("input[name='password2']").val();
	var bcod = $("input[name='bcod']").val();

    var json = {name: name, surname: surname, mail: email, password: password, bcod: bcod};
	if(password!==password2) {
		alert('The two passwords don\'t match.')	;
		event.preventDefault();
	} else if (password.length < 8) {
        alert('Password must be at least of 8 characters!');
        event.preventDefault();
    } else {	
    	$.ajax("/rest_api/v1.0/signup",
        	{
            	method: 'POST',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
            	success: function (data, status) {
					var first = "y";
    				'<%Session["first"] = "' + first + '"; %>';
                    window.location='settings.html'
                },
				error: function(xhr, textStatus, errorThrown) {
       				alert('There was an error and it was impossible to create the new user. Maybe you inserted a wrong bracelet code, check it!');
    			}
        	 }
    	);
	}
    //avoid form submission (the default action of the event)
    event.preventDefault();
}