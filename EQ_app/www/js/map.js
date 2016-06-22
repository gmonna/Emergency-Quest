// JavaScript Document
// JavaScript Document
$(document).ready(function () {
    get_position();
});

function get_position() {
    $.ajax(
        'http://192.168.1.102:8080/rest_api/v1.0/get_position',
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