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
				var colour = ""; var song = ""; var auto_clean = ""; var doc_access = "";
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
				
				switch (settings.auto_clean) {
				case "y":
					auto_clean = 2;
					break;
				case "n":
					auto_clean = 1;
					break; 	
				}
				
				switch (settings.doc_access) {
				case "y":
					doc_access = 1;
					break;
				case "n":
					doc_access = 0;
					break; 	
				}
				
               	document.getElementById("radius-field").value = settings.perimeter;
				$("#colourdiv-"+song).addClass("checked");
				$("#musicdiv-"+song).addClass("checked");
				document.getElementById("colour-"+colour).checked = true;
				document.getElementById("song-"+song).checked = true;
				document.getElementById("mess-field").value = settings.message;
               	document.getElementById("doc-field").value = settings.doct;
				$("#autocleandiv-"+auto_clean).addClass("checked");
				$("#docaccessdiv-"+doc_access).addClass("checked");
				document.getElementById("auto_clean-"+settings.auto_clean).checked = true;
				document.getElementById("doc_access-"+settings.doc_access).checked = true;
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
	var doc = $("input[name='doc_access']:checked").val();

    var json = {perimeter: perimeter, message: message, doct: doct, colour: colour, song: song, auto_clean: auto, doc_access:doc};

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