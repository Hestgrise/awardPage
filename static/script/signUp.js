console.log("Account creation validation JavaScript is working")
document.addEventListener('DOMContentLoaded', buttonSet);
var url = 'http://ec2-52-26-46-121.us-west-2.compute.amazonaws.com:5423/createUserAccount';
//var url ='http://127.0.0.1:5423/createUserAccount';

function buttonSet() {
	var submitButton = document.getElementById('createAccountButton');

	submitButton.onclick = function(event) {
		if (validateForm()) {
			var createRequest = new XMLHttpRequest();
			var accountInfo = {firstName:document.getElementsByName("firstName")[0].value,
				lastName:document.getElementsByName("lastName")[0].value,
				email:document.getElementsByName("email")[0].value,
				password:document.getElementsByName("password")[0].value,
				signatureFile:document.getElementsByName("signatureFile")[0].value};
			var payload = JSON.stringify(accountInfo);

			createRequest.open('POST', url, true);
			createRequest.setRequestHeader('Content-Type', 'application/json');
			createRequest.addEventListener('load', function() {
				if (createRequest.status >= 200 && createRequest.status < 400) {
					var response = JSON.parse(createRequest.responseText);
					document.getElementById('registerResult').textContent = response.message;
					//Check for substring in response indicating successful account creation
					//Change color of response message to green if found
					if (response.message.indexOf("success") != -1) {
						document.getElementById('registerResult').style.color = "green";
					}
				} else {
					document.getElementById('registerResult').textContent = "Server is unreachable at this time";
				}
			});

			createRequest.send(payload);
			event.preventDefault();
		}
		else {
			document.getElementById('registerResult').textContent = "You must fill out all fields and upload a file.";
		}
	}
}

function validateForm() {
	var email = document.getElementsByName("email")[0].value;
	var fName = document.getElementsByName("firstName")[0].value;
	var lName = document.getElementsByName("lastName")[0].value;
	var password = document.getElementsByName("password")[0].value;
	//var file = document.getElementsByName("signatureFile");

	if (email == null || email == "" || fName == null || fName == "" 
		|| lName == null || lName == "" || password == null || password == "") {
		return false;
	}
	return true;
}
