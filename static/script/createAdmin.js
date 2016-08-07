console.log("Account creation validation JavaScript is working")
document.addEventListener('DOMContentLoaded', buttonSet);
var url ='../createAdminAccount';

function buttonSet() {
	var submitButton = document.getElementById('createAdminButton');

	submitButton.onclick = function(event) {
		var createRequest = new XMLHttpRequest();
		
		var form = document.getElementById('createAccountForm');
		var formData = new FormData(form);
		
		createRequest.open('POST', url, true);
		createRequest.addEventListener('load', function() {
			if (createRequest.status >= 200 && createRequest.status < 400) {
				var response = JSON.parse(createRequest.responseText);
				document.getElementById('registerResult').textContent = response.message;
				//Check for substring in response indicating successful account creation
				//Change color of response message to green if found
				if (response.message.indexOf("success") != -1) {
					document.getElementById('registerResult').style.color = "green";
					window.location = '/admins.html';
				}
				else {
					document.getElementById('registerResult').style.color = "red";
				}
			} else {
				document.getElementById('registerResult').textContent = "Server is unreachable at this time";
			}
		});

		createRequest.send(formData);
		event.preventDefault();
	}
}
