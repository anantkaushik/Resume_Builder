$(function(){
	$.validate({
        modules : 'security'
    });
})
$("#signin-btn").click(function(){
    $("#login-form").show();
    $("#signup-form").hide();
});
$("#signup-btn").click(function(){
    $("#login-form").hide();
    $("#signup-form").show();
});