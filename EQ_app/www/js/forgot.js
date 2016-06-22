// JavaScript Document
$(document).ready(function () {
    //set what happens when the "Enter" button is pressed
    $('form#forgot-form').submit(function (event) {
        forgot(event);
    });
});

function forgot(event) {
    var email = $("input[name='email']").val();

    var json = {email: email};
        $.ajax("http://192.168.1.102:8080/rest_api/v1.0/lost_password",
            {
                method: 'POST',

                contentType: 'application/json',
                data: JSON.stringify(json),

                success: function (data, status) {
					alert('An e-mail has been sent to your account, check it!')
                    setTimeout(function () {
       					window.location.assign("login.html");
    				}, 2000);
                },
				error: function(xhr, textStatus, errorThrown)	{
       				alert('The inserted e-mail is not linked to any account.');
    			}
            }
        );

        //avoid form submission (the default action of the event)
   event.preventDefault();
}