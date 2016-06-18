// JavaScript Document
var code;
$(document).ready(function () {
	get_if_code();
	if (code!=-1) {
		get_appointment(code);	
		$('form#appo-form').submit(function (event) {
        	update_appointment(event, code);
    	});
	} else {
		$('form#appo-form').submit(function (event) {
        	set_appointment(event);
    	});
	}
});

function get_appointment(code) {
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/calendar/'+code,
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var appointment = data.appointment;
                document.getElementById("title-field").value = appointment.title;
        		document.getElementById("description-2").value = appointment.description;
				document.getElementById("data-field").value = appointment.data;
				document.getElementById("ora-field").value = appointment.ora;
                document.getElementById("message-field").value = appointment.message;
				document.getElementById("node-"+appointment.priority).checked = true;
			},
			error: function(xhr, textStatus, errorThrown) {
       			alert('Unknown error, charging this appointment was impossible.');
    		}
        }
    );
}

function get_if_code() {
	$.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/get_if_code',
        {
            method: "GET",
            dataType: "json",
			async:false,
            success: function (data, status) {
				code = data.code;
			},
			error: function(xhr, errorThrown) {
				code = -1;
			}
        }
    );
}

function update_appointment(event, code) {
	var title = $("input[name='title']").val();
	var description = $("input[name='description']").val();
    var date = $("input[name='data']").val();
    var hour = $("input[name='ora']").val();
	var message = $("input[name='message']").val();
	var priority = $("input[name='Radio3']:checked").val();

    var json = {code: code, title: title, description: description, data: date, ora: hour, message: message, priority: priority};

    	$.ajax("http://127.0.0.1:5000/rest_api/v1.0/calendar/"+code,
        	{
            	method: 'PUT',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
            	success: function (data, status) {
					alert('Appointment successfully updated.');
                },
				error: function(xhr, textStatus, errorThrown) {
       				alert('There was an unknown error and it was impossible to update appointment.');
    			}
        	 }
    	);
    //avoid form submission (the default action of the event)
    event.preventDefault();
}

function set_appointment(event) {
	var title = $("input[name='title']").val();
	var description = $("input[name='description']").val();
    var date = $("input[name='data']").val();
    var hour = $("input[name='ora']").val();
	var message = $("input[name='message']").val();
	var priority = $("input[name='Radio3']:checked").val();

    var json = {title: title, description: description, data: date, ora: hour, message: message, priority: priority};

    	$.ajax("http://127.0.0.1:5000/rest_api/v1.0/calendar/insert",
        	{
            	method: 'POST',
            	contentType: 'application/json',
            	data: JSON.stringify(json),
            	success: function (data, status) {
					alert(data);
                },
				error: function(xhr, textStatus, errorThrown) {
       				alert('There was an unknown error and it was impossible to save appointment.');
    			}
        	 }
    	);
    //avoid form submission (the default action of the event)
    event.preventDefault();
}