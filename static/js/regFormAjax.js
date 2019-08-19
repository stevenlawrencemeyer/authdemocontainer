$(document).ready(function() {


// AJAX FOR EMAIL *************************************************    
    
$(".slm-form-container form #id_email").change(function() {
    let testVar = $(this).val();
    //alert(testVar);
    let xElem = ".slm-form-container form #id_email";
    let checkVar = 'email';
    //alert('checkvar= ' + checkvar);
    let msg = '<span id="email-duplicate"><br>A user with this email already exists<br>';
    msg+= 'Did you forget your password, dimwit?';
    msg+= '<br><a href="/accounts/password-reset">Reset password</a></span>';
    formAjax(testVar, xElem, checkVar, msg);
}); // end email change


$(".slm-form-container form #id_alt_email").change(function() {
    let testVar = $(this).val();
    //alert(testVar);
    let xElem = ".slm-form-container form #id_alt_email";
    let checkVar = 'email';
    let msg = '<span id="email-duplicate"><br>A user with this email already exists<br>';
    msg+= 'Did you forget your password, dimwit?';
    msg+= '<br><a href="/accounts/password-reset">Reset password</a></span>';
    formAjax(testVar, xElem, checkVar, msg);
}); // end email change
  
  
   
$(".slm-form-container form #id_display_username").change(function() {
    let testVar = $(this).val();
    //alert(testVar);
    let xElem = ".slm-form-container form #id_display_username";
    let checkVar = 'username';
    let msg = '<span id="email-duplicate"><br>A user with this username already exists<br>';
    msg+= 'Did you forget your password, dimwit?';
    msg+= '<br><a href="/accounts/password-reset">Reset password</a></span>';
    formAjax(testVar, xElem, checkVar, msg);
}); // end display username change


    
//This does the Ajax processing
//If the display_username or email exists we insert
//an error message
//Otherwise we remove any existing error message
//There is an overhead in doing this validation
//It may be necessary to index the email addresses
//and display usernames for a very large database
function formAjax(testVar, xElem, checkVar, msg) {

        $.ajax({
            // url relates to path in accounts/urls.py
            //It is the equivalent of accounts:url
            //in Django
            url: 'http://localhost:8000/accounts/validate-user',  
            data: {'testvar':testVar, 'checkvar':checkVar},
            dataType: 'json',
            success:function(data) {
                if(data.is_taken){
                    elem = $(xElem);
                    elem.focus();
                    $(msg).insertAfter(elem);
                }// end if
                else {
                    $("span[id='email-duplicate']").remove();
                    //$(xElem).focus();
                    
                }// end else
                
                
            }// end success function
            
        }); // end ajax
}; // end function formAjax
    

    
});// end ready
