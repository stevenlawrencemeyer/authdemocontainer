$(document).ready(function() {
    
   
    $(window).keydown(function(e){
        if (e.keydown == 13) {
            e.preventDefault();
            return false;
            
        }; // end if
        
    }); // end keydown


// jQuery Validation Plugin  https://jqueryvalidation.org/
   
$(".slm-form-container form").validate({
    rules: {
        old_password: {
            required:true
        },// end old password
        new_password1: {
            required: true,
            minlength: 8
        },
        new_password2: {
            required: true,
            minlength: 8,
            equalTo: "#id_new_password1"
        }
        
    },// end rules
    messages: {
        new_password2: {
            equalTo: "Passwords don't match"
        }
    }// end messages
    
});// end validate
    
       

    
})// end ready