// JavaScript Document
// JavaScript Document
$(document).ready(function () {
    get_position();
});

function get_position() {
    $.ajax(
        '/rest_api/v1.0/get_position',
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
       				alert('Unknown error, charging past position during this day was impossible.');
    		}
        }
    );
}