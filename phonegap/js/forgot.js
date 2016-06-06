// JavaScript Document
$(document).ready(function () {
    //set what happens when the "Enter" button is pressed
    $('form#submit-form').submit(function (event) {
        forgot(event);
    });
});

function forgot(event) {
    var email = $("input[name='mail']").val();

    var json = {mail: email};
        $.ajax("/rest_api/v1.0/lost_password",
            {
                method: 'GET',

                contentType: 'application/json',
                data: JSON.stringify(json),

                success: function (data, status) {
					alert('An e-mail has been sent to your account, check it!')
                    setTimeout(function () {
       					window.location.href = "login.html";
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