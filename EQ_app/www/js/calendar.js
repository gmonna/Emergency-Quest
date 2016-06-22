// JavaScript Document
$(document).ready(function () {
	'<%Session["code"] = "-1"; %>'
    get_calendar();
});

function get_calendar() {
    $.ajax(
        'http://192.168.1.102:8080/rest_api/v1.0/get_calendar',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var calendar = data.calendar;
				for (var i = 0; i < calendar.length; i++) {
					var code = calendar[i].code;
					var done = calendar[i].done;
					var title = calendar[i].title;
					var data = calendar[i].data;
               	  	var ora = calendar[i].ora;
					
					switch(done) {
					case "y":
						check = "highlighted";
						goz = "";
						break;
					case "n":
						check = "";
						goz = "go";
						break;
					}
	              	$("ul#calendar-list").append('<li class="list-item grey '+check+'" data-ix="list-item" style="opacity: 1; transform: translateX(0px) translateY(0px); transition: opacity 500ms cubic-bezier(0.23, 1, 0.32, 1), transform 500ms cubic-bezier(0.23, 1, 0.32, 1);"><a class="w-clearfix w-inline-block '+check+' '+goz+'" code="'+code+'"><div class="icon-list '+check+'"><div class="icon ion-ios-checkmark-empty"></div></div><div class="title-list">'+title+'</div><div class="sub-title-small" style="color: inherit;">'+data+'&nbsp;|&nbsp;'+ora+'</div></a><div class="right-list"><a class="delete" code="'+code+'" style="color: inherit;"><div class="icon ion-ios-close-empty"></div><a></div></li>');
					
					$("a.delete").click(function (event) {
		           		var code=$(this).attr('code');
                   		delete_appointment(code);
               		});
					
					$("a.go").click(function (event) {
               		 	var code=$(this).attr('code');
               		  	show_appointment(code);
               		});
				}
			},
			error: function(xhr, errorThrown) {
				$("ul#calendar-list").append("<li><p>No appointments.</p><li>");	
			}
        }
    );
}

function show_appointment(code) {
	var json = {code: code};
	$.ajax("http://192.168.1.102:8080/rest_api/v1.0/store_if_code",
        {
           	method: 'POST',
           	contentType: 'application/json',
           	data: JSON.stringify(json),
           	success: function (data, status) {
            	window.location.assign('manageappo.html');
			}, error: function(xhr, errorThrown) {
				alert('Impossible to load this appointment.');	
			}
        }
    );		
}

function store_code(code) {
	
}

function delete_appointment(code) {
	var r = confirm("Are you sure you want to delete this appointment?");
	if (r==true) {
    	$.ajax("http://192.168.1.102:8080/rest_api/v1.0/calendar/"+code,
        	{
           		method: 'DELETE',
            	success: function (status) {
                	// update the list of appointments
                	location.reload();
            	}
        	}
    	);
	}
}