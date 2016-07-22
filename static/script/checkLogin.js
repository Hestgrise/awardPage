console.log("Login validation JavaScript is working")
document.addEventListener('DOMContentLoaded', buttonSet);
var url = 'http://ec2-52-26-46-121.us-west-2.compute.amazonaws.com:5423/';
//var url = 'http://127.0.0.1:5423/'

function buttonSet() {
	var submitButton = document.getElementById('loginButton');

	submitButton.onclick = function(event) {
		var createRequest = new XMLHttpRequest();
		var loginInfo = {email:document.getElementsByName("email")[0].value,
			password:document.getElementsByName("password")[0].value};
		var payload = JSON.stringify(loginInfo);

		createRequest.open('POST', url + 'checkLogin', true);
		createRequest.setRequestHeader('Content-Type', 'application/json');
		createRequest.addEventListener('load', function() {
			if (createRequest.status >= 200 && createRequest.status < 400) {
				var response = JSON.parse(createRequest.responseText);
				document.getElementById('loginResult').textContent = response.message;
				//Check for substring in response indicating successful account creation
				//Redirect to user's home page if found
				if (response.message.indexOf("success") != -1) {
					document.getElementById("loginResult").style.color = "green";
					window.location = url + 'dashboard.html';
				} 
			}
			else {
				document.getElementById('loginResult').textContent = "Server is unreachable at this time";
			}
		});

		createRequest.send(payload);
		event.preventDefault();
	}
}