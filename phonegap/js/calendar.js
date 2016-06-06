// JavaScript Document
$(document).ready(function () {
    get_calendar();
});

function get_calendar() {
    $.ajax(
        '/rest_api/v1.0/get_calendar',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var calendar = data.calendar;
				for (var i = 0; i < calendar.length; i++) {
					var code = calendar[i].code;
					var done = calendar[i].done;
					var titolo = calendar[i].title;
					var data = calendar[i].data;
                    var ora = calendar[i].ora;
					
					switch(done) {
					case "y":
						check = "highlighted";
						break;
					case "n":
						check = "";
						break;
					}
					
                    $("ul#calendar-list").append("<li class=\"list-item grey "+
						check+"\" data-ix=\"list-item\"><a class=\"w-clearfix w-inline-block show\" code=\""+
						code+"\"><div class=\"icon-list "+
						check+"\"><div class=\"icon ion-ios-checkmark-empty\"></div></div><div class=\"title-list "+
						check+"\">"+
						titolo+"</div><div class=\"sub-title-small\" style=\"color: inherit;\">"+
						data+" &nbsp;|&nbsp; "+
						ora+"</div></a><div class=\"right-list\"><a class=\"delete\" code=\""+
						code+"\" style=\"color: inherit;\"><div class=\"icon ion-ios-close-empty\"></div><a></div></li>");
					
					$("a.delete").click(id, function (event) {
                    	var code=$(this).attr('code');
                    	delete_appointment(code);
                	});
					
					$("a.show").click(id, function (event) {
                    	var code=$(this).attr('code');
                    	show_appointment(code);
                	});
				}
			},
			error: function(xhr, textStatus, errorThrown) {
       				alert('Unknown error, charging history was impossible.');
    		}
        }
    );
}

function show_appointment(code) {
	'<%Session["code"] = "' + code + '"; %>'
	window.location('manageappo.html');	
}

function delete_appointment(code) {
    $.ajax("/rest_api/v1.0/calendar/"+code,
        {
            method: 'DELETE',
            success: function (status) {
                // update the list of appointments
                get_calendar();
            }
        }
    );
}