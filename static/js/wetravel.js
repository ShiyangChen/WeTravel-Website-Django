$(document).ready(function(){
		var dialog, form;

		function changeAddress() {

		}

        dialog = $('#dialog-form').dialog({
          autoOpen: false,
          width: '500px',
          resize: "auto",
          modal: true,
          buttons: {
          	"Change": changeAddress,
          	Cancel: function() {
          		dialog.dialog("close");
          	}
          },
          close: function() {
          	form[0].reset();
          	allFields.removeClass("ui-state-error");
          },
          
        });

        form = dialog.find("form").on("submit", function(event) {
        	event.preventDefault();
        	//changeAddress();
        })

        $(".edit").click(function(){
          dialog.dialog('open');
          return false;
        });
});