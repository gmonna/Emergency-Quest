// JavaScript Document
// JavaScript Document
var counter = 1
$(document).ready(function () {
	counter = 1;
    get_position();
});


function get_position() {
	
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/get_position',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var position = data.position;
				var latitude = position.latitude;
				var longitude = position.longitude;
				
				$("#mappp").attr({
        			"data-widget-latlng" : latitude + "," + longitude
    			});
				
			},
			error: function(xhr, textStatus, errorThrown) {
       				alert('Unknown error, charging position is impossible.');
    		}
        }
    );
}