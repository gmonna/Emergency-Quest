// JavaScript Document
$(document).ready(function () {
    logout();
});

function logout() {
    $.ajax(
        'http://192.168.1.102:8080/rest_api/v1.0/logout',
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