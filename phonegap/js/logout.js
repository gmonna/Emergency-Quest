// JavaScript Document
$(document).ready(function () {
    logout();
});

function logout() {
    $.ajax(
        '/rest_api/v1.0/logout',
        {
            method: "GET",
            success: function (status) {
				window.location('login.html');
			},
			error: function(xhr, textStatus, errorThrown) {
       			alert('Unknown error, logging out was impossible.');
    		}
        }
    );
}