// JavaScript Document
$(document).ready(function () {
    get_history();
});

function get_history() {
    $.ajax(
        '/rest_api/v1.0/get_history',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var history = data.history;
				for (var i = 0; i < history.length; i++) {
					var read = history[i].read;
					var data = history[i].data;
                    var ora = history[i].ora;
                    var message = tasks[i].message;
					
					switch(read) {
					case "y":
						circle = "<i class=\"ion-record\" style=\"color: #bababa\"></i>";
						break;
					case "n":
						circle = "<i class=\"ion-record\" style=\"color: #ffde47\"></i>";
						break;
					}

                    $("ul#history-list").append("<li class=\"list-item-new\"><div class=\"text-new\"><h2 class=\"title-new\">"+
						circle+"</h2><p class=\"description-new\">"+
						message+"</p><div class=\"sub-title-small\" style=\"color: inherit;\">"+
						data+" &nbsp;|&nbsp; "+
						ora+"</div></div></li>");
				}
			},
			error: function(xhr, textStatus, errorThrown) {
       				alert('Unknown error, charging history was impossible.');
    		}
        }
    );
}
