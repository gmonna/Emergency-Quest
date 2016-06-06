// JavaScript Document
$(document).ready(function () {
	check_login();
    //set what happens when the "Enter" button is pressed
    $('form#submit-form').submit(function (event) {
        login(event);
    });
});

function check_login() {
	$.ajax("/rest_api/v1.0/already_signin",
            {
                method: 'GET',

                contentType: 'application/json',

                success: function (data, status) {
                    window.location='maps.html'
                }
            }
        );
}

function login(event) {
    var email = $("input[name='email']").val();
    var password = $("input[name='password']").val();

    var json = {mail: email, password: password};
        $.ajax("/rest_api/v1.0/signin",
            {
                method: 'GET',

                contentType: 'application/json',
                data: JSON.stringify(json),

                success: function (data, status) {
                    window.location='maps.html'
                },
				error: function(xhr, textStatus, errorThrown)	{
       				alert('The inserted e-mail is not linked to any account.');
    			}
            }
        );

   //avoid form submission (the default action of the event)
   event.preventDefault();
}