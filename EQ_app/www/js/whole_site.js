// JavaScript Document
$(document).ready(function () {
    get_numbers();
	setInterval(function() {
  		send_position();
	}, 60*1000);
});

function get_numbers() {
    $.ajax(
        'http://192.168.1.102:8080/rest_api/v1.0/get_numbers',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var numbers = data.numbers;
				document.getElementById("his").innerHTML = numbers.history;
				document.getElementById("cal").innerHTML = numbers.calendar;
				if(data.patient=='y') {
					document.getElementById("logout").style.display = 'none';	
				}
			},
			error: function(xhr, textStatus, errorThrown) {
       				document.getElementById("his").innerHTML = "0";
					document.getElementById("cal").innerHTML = "0";
					alert('Unknown error during connection with database');
    		}
        }
    );
}

function send_position() {
	navigator.geolocation.getCurrentPosition(function(location) {
  		var latitude = location.coords.latitude;
  		var longitude = location.coords.longitude;
		var json = {latitude:latitude, longitude:longitude};
    	$.ajax("http://192.168.1.102:8080/rest_api/v1.0/set_position/",
        	{
            	method: 'POST',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
            	error: function(xhr, textStatus, errorThrown) {
					alert('It was impossible to send your position, maybe you turned off localization.');
    			}
        	 }
    	);
	});
}
