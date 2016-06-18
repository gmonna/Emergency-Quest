// JavaScript Document
$(document).ready(function () {
    get_numbers();
});

function get_numbers() {
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/get_numbers',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var numbers = data.numbers;
				document.getElementById("his").innerHTML = numbers.history;
				document.getElementById("cal").innerHTML = numbers.calendar;
			},
			error: function(xhr, textStatus, errorThrown) {
       				document.getElementById("his").innerHTML = "0";
					document.getElementById("cal").innerHTML = "0";
					alert('Unknown error during connection with database');
    		}
        }
    );
}
