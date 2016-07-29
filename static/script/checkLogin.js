console.log("Login validation JavaScript is working")
document.addEventListener('DOMContentLoaded', buttonSet);
var url = '../'

function buttonSet() {
	var submitButton = document.getElementById('loginButton');

	submitButton.onclick = function(event) {
		var createRequest = new XMLHttpRequest();
		// set POST request parameters
		var loginInfo = {email:document.getElementsByName("email")[0].value,
			password:document.getElementsByName("password")[0].value,
			accountType:document.getElementsByName("accountType")[0].value};
		var payload = JSON.stringify(loginInfo);
		// submits a post request to login
		createRequest.open('POST', url + 'checkLogin', true);
		createRequest.setRequestHeader('Content-Type', 'application/json');
		createRequest.addEventListener('load', function() {
			if (createRequest.status >= 200 && createRequest.status < 400) {
				var response = JSON.parse(createRequest.responseText);
				document.getElementById('loginResult').textContent = response.message;
				//Check for substring in response indicating successful login
				//Redirect to either the admin or user's home page
				if (response.message.indexOf("success") != -1) {
					document.getElementById("loginResult").style.color = "green";
					if (response.message.indexOf("Admin") != -1)
						window.location = url + 'admin_dashboard.html';
					else
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