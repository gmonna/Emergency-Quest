// JavaScript Document
$(document).ready(function () {
    logout();
});

function logout() {
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/logout',
        {
            method: "GET",
            success: function (status) {
				window.location.assign('login.html');
			},
			error: function(xhr, textStatus, errorThrown) {
       			alert('Unknown error, logging out was impossible.');
    		}
        }
    );
}