// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
	// console.log('statusChangeCallback');
	// console.log(response);

	// var userID = FB.getAuthResponse().userID;
	// var accessToken = FB.getAuthResponse().accessToken;

	if (FB.getAuthResponse()) {
		// console.log(FB.getAuthResponse().userID);
		// console.log(FB.getAuthResponse().accessToken);
	} else {
		// console.log('User is not logged in');
	}

	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		$('#btn_login').css('display', 'none');
		$('#btn_confirm').css('display', 'inline-block');
		$('#btn_delete').css('display', 'none');
		// Logged into your app and Facebook.
		testAPI();
		// Send user's info to serverside.
		// sendUserInfo();
	} else {
		// The person is not logged into your app or we are unable to tell.
		document.getElementById('status').innerHTML = 
		'After entering your email address, Please log in by click Facebook Login button';
	}
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

// Logout from FB
function fbLogout() {
	var userID = FB.getAuthResponse().userID;
	var accessToken = FB.getAuthResponse().accessToken;

	FB.logout(function(response) {

		/* make the API call */
		// FB.api(
		// 	"/" + userID + "/permissions?access_token=" + accessToken,
		// 	"DELETE",
		// 	function (response) {
		// 		if (response && !response.error) {
		// 			/* handle the result */
		// 			console.log(response);
		// 		} else {
		// 			console.log(response.error);
		// 		}
		// 	}
		// );

		// Person is now logged out
		document.getElementById('status').innerHTML = 
		'After entering your email address, Please log in by click Facebook Login button';
		$('#btn_login').css('display', 'block');
		$('#btn_confirm').css('display', 'none');
		$('#btn_delete').css('display', 'none');
		$('#email_form').css('display', 'block');
		document.getElementById('email_address').value = '';
	});
}

window.fbAsyncInit = function() {
	FB.init({
		appId      : '1633923886632047',
		cookie     : true,
		xfbml      : true,
		version    : 'v2.11'
	});

	FB.AppEvents.logPageView();

	// Now that we've initialized the JavaScript SDK, we call 
	// FB.getLoginStatus().  This function gets the state of the
	// person visiting this page and can return one of three states to
	// the callback you provide.  They can be:
	//
	// 1. Logged into your app ('connected')
	// 2. Logged into Facebook, but not your app ('not_authorized')
	// 3. Not logged into Facebook and can't tell if they are logged into
	//    your app or not.
	//
	// These three cases are handled in the callback function.

	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});	
};

// Load the SDK asynchronously
(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement(s); js.id = id;
	js.src = "https://connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function testAPI() {
	var username = '';
	// console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		// console.log('Successful login for: ' + response.name);
		document.getElementById('status').innerHTML =
		'Thanks for logging in, <b>' + response.name + '</b>!<br>'
		+ 'From now on, you can get "Diana-Notification" once a day<br>'
		+ 'First notification will be sent in an hour<br>'
		+ 'Thank you for using Diana!';
		sendUserInfo(response.name);
	});
}