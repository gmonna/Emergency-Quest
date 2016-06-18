// JavaScript Document
$(document).ready(function () {
    get_settings();

    $('form#settings-form').submit(function (event) {
        set_settings(event);
    });
});

function get_settings() {
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/get_settings',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var settings = data.settings;
				var colour = ""; var song = "";
				switch (settings.colour) {
				case "blue":
					colour = 3;
					break;
				case "red":
					colour = 2;
					break;
				case "yellow":
					colour = 1;
					break;
				}
				switch (settings.song) {
				case "relax":
					song = 3;
					break;
				case "concentrate":
					song = 2;
					break;
				case "remind":
					song = 1;
					break;
				}
               	document.getElementById("radius-field").value = settings.perimeter;
				document.getElementById("colour-"+colour).checked = true;
				document.getElementById("song-"+song).checked = true;
				document.getElementById("mess-field").value = settings.message;
               	document.getElementById("doc-field").value = settings.doct;
				document.getElementById("auto_clean-"+settings.auto_clean).checked = true;
			},
			error: function(xhr, errorThrown) {
				alert('No settings.');	
			}
        }
    );
}

function set_settings(event) {
	var perimeter = $("input[name='radius']").val();
	var message = $("input[name='message']").val();
    var doct = $("input[name='doctor']").val();
    var colour = $("input[name='colour']:checked").val();
	var song = $("input[name='song']:checked").val();
	var auto = $("input[name='auto_clean']:checked").val();

    var json = {perimeter: perimeter, message: message, doct: doct, colour: colour, song: song, auto_clean: auto};

    	$.ajax("http://127.0.0.1:5000/rest_api/v1.0/set_settings",
        	{
            	method: 'POST',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
            	success: function (data, status) {
					alert('Settings successfully updated.');
                },
				error: function(xhr, textStatus, errorThrown) {
       				alert('There was an unknown error and it was impossible to change settings.');
    			}
        	 }
    	);
    //avoid form submission (the default action of the event)
    event.preventDefault();
}