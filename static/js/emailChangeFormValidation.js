$(document).ready(function() {
    
    $(window).keydown(function(e){
        if (e.keydown == 13) {
            e.preventDefault();
            return false;
            
        }; // end if
        
    }); // end keydown
    
    $('.slm-form-container form :input:enabled:visible:first').focus();

   // $("#slm-submit").on("click", function(e){
        //e.preventDefault();
        //$("#id-password1").attr("type", "password");
        //$("form").submit();

    //})


// jQuery Validation Plugin  https://jqueryvalidation.org/
   
$(".slm-form-container form").validate({
    rules: {
        email: {
            email: true
        },// end email
        
        alt_email: {
            email: true
        },
        
    },// end rules

    
})// end validate
    

   
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
    
 
   
    
    

    
})// end ready