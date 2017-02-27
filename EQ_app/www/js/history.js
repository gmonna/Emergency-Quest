// JavaScript Document
$(document).ready(function () {
    get_history();
});

function get_history() {
    $.ajax(
        'http://127.0.0.1:5000/rest_api/v1.0/get_history',
        {
            method: "GET",
            dataType: "json",
            success: function (data, status) {
                var history = data.history;
				for (var i = 0; i < history.length; i++) {
					var read = history[i].read;
					var data = history[i].data;
                   	var ora = history[i].ora;
                   	var message = history[i].message;
				
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
			error: function(xhr, errorThrown) {
				$("ul#history-list").append("<li><p>No history.</p><li>");		
			}
        }
    );
}
