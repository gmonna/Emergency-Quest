// JavaScript Document
$(document).ready(function () {
    check_login();
});

function check_login() {
	$.ajax("http://127.0.0.1:5000/rest_api/v1.0/already_signin",
            {
                method: 'GET',

                contentType: 'application/json',
				
				statusCode: {
     				300: function (response) {
         				$("#main-stack").attr({
        					"data-redirect" : "login.html"
    					});
      				},
				},

                success: function (data, status) {
                    $("#main-stack").attr({
        				"data-redirect" : "map.html"
    				});
                }
            }
        );
}