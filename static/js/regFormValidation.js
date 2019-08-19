$(document).ready(function() {
 // prevents form submission when pressing enter   
    $(window).keydown(function(e){
        if (e.keydown == 13) {
            e.preventDefault();
            return false;
            
        }; // end if
        
    }); // end keydown -- 
    
    
    // focuses on first field in form
    $('.slm-form-container form :input:enabled:visible:first').focus();


    // toggles visibility of password fields
    $("#pw-toggle").click(function() {
     
        let fld1 = $('.slm-form-container input[id*="password1"]');
        let fld2 = $('.slm-form-container input[id*="password2"]');
        //let fld1 = $("#id_password1")
        //let fld2 = $("#id_password2")
        let xtype = fld1.attr("type");
        if (xtype=="password") {
            fld1.attr("type", "input");
            fld2.attr("type", "input");
        } else {
            fld1.attr("type", "password");
            fld2.attr("type", "password");
        }
        
        $("#id_password1").focus()
    }) // end pw-toggle


// jQuery Validation Plugin  https://jqueryvalidation.org/
   
$(".slm-form-container form").validate({
    rules: {
        email: {
            required: true,
            email: true
        },// end email
        password1: {
            required: true,
            minlength: 8
        },
        password2: {
            required: true,
            minlength: 8,
            equalTo: "#id_password1"
        },
        username: {
            required: true,
        },
        first_name: {
            required: true
        },
        last_name: {
            required: true
        },
        
        alt_email: {
            email:true,
            required:false
        }
        
    },// end rules
    messages: {
        password2: {
            equalTo: "Passwords don't match dimwit"
        }
    }
    
})// end validate
    

   // applies regular expressions to alpha fields
    var regex1 = /^[a-zA-z -]+$/
    var regex2 = /^[a-zA-z0-9- ]+$/
    
    fld = "#id_username";
    $(".slm-form-container .alpha").change(function() {
        let x = $(this).val();
        let id = $(this).attr("id");
        let regex = regex1;
        let msg = "Only letters, spaces and hyphens allowed"
        if (id == "id_display_username") {
            regex = regex2;
            msg = "only, letters, numbers, spaces and hyphens allowed"
        }; 
        
        msg = '<p id="alpha-msg">' + msg + '</p>'; 
        let y = x.match(regex);
        if (y == null) {
            $(this).parent("p").after(msg);
            $(this).focus();
        } else {
            $('p[id="alpha-msg"]').remove();
            
        };

    
    })// end focusout
    
    // checks whether passwords equal
    $(".slm-form-container input").change(function() {

        let x1 = $("#id_password1").val();
        var x2 = $("#id_password2").val();
        if (x1 == x2) {
            $('label[id*="id_password2-error"]').remove();
        }
        
        
    })// end function form container
   
 
    

    
})// end ready