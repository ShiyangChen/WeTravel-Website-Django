$(document).ready(function(){
		var profile_image_dialog, profile_image_form, address_dialog, address_form;

    //Change Profile Image
    //---------------------------------------------------------------------
     profile_image_dialog = $('#dialog-profile-image-form').dialog({
      autoOpen: false,
      width: '500px',
      resize: "auto",
      modal: true,
      buttons: {
        "Upload": function() {
          profile_image_form.submit();
          profile_image_dialog.dialog("close");
        },
        Cancel: function() {
          profile_image_dialog.dialog("close");
        }
      },
      close: function() {
        profile_image_form[0].reset();
        allFields.removeClass("ui-state-error");
      },
      
    });

    profile_image_form = profile_image_dialog.find("form");
    
    profile_image_form.submit(function() {
      event.preventDefault();
      var file = $('#id_image').get(0);
      var formData = new FormData();
      formData.append('profile-image', file, file.name);

      $.ajax({
          type: profile_image_form.attr('method'),
          url: profile_image_form.attr('action'),
          data: formData,
          processData: false,
          contentType: false,
          success: function(json) {
            console.log(json); // log the returned json to the console
            console.log("success")
          }, 
          error: function(json) {
            console.log(json); // log the returned json to the console
            console.log("faile")
          }
          //error: function(xhr,errmsg,err) {
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          //}
      });
      return false;
    });

    $("#change-profile-image").click(function(){
      profile_image_dialog.dialog('open');
      return false;
    });


    //Change Address Information
    //---------------------------------------------------------------------------
    address_dialog = $('#dialog-address-form').dialog({
      autoOpen: false,
      width: '500px',
      resize: "auto",
      modal: true,
      buttons: {
      	"Change": function() {
          address_form.submit();
          address_dialog.dialog("close");
        },
      	Cancel: function() {
      		address_dialog.dialog("close");
      	}
      },
      close: function() {
      	address_form[0].reset();
      	allFields.removeClass("ui-state-error");
      },
      
    });

    address_form = address_dialog.find("form");
    address_form.submit(function() {
      event.preventDefault();

      $.ajax({
          type: address_form.attr('method'),
          url: address_form.attr('action'),
          data: address_form.serialize(),
          success: function(json) {
            $('#dd-country').text(json.country);
            $('#dd-state').text(json.state);
            $('#dd-city').text(json.city);

            console.log(json); // log the returned json to the console
            console.log("success")
          }, 
          error: function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
      return false;
    });

    $("#change-address").click(function(){
      address_dialog.dialog('open');
      return false;
    });

   

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});