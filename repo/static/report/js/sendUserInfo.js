function sendUserInfo(name) {

    $('#email_form').css('display', 'none');

    var params = {
        userID: FB.getAuthResponse().userID,
        accessToken: FB.getAuthResponse().accessToken,
        email: $('#email_address').val(),
        username: name
    }

    // console.log(params);

    $.ajax({
        type: "post",
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        // dataType: 'json',
        crossDomain: true,
        url: "/gen_access_token",
        data: params,
        error: function(msg){
            // console.log("error: " + msg);
        },
        success: function(data){
            // console.log('response from server: ');

            if (data == "no email!") {
                fbLogout();
                document.getElementById('validation').innerHTML = 
                "Please enter your email address correctly";
                $('#email_address').value = '';
            }
            // console.log(data);

            // Graph API 사용 시작

        }
    });
}

