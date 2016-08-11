console.log("Account creation validation JavaScript is working");
document.addEventListener('DOMContentLoaded', buttonSet);
var url ='../createUserAccount';
//Credit for some asistance with JavaScript code implementation to Professor Wolford CS 290 Lectures 
function buttonSet() {
	var submitButton = document.getElementById('createAccountButton');

	submitButton.onclick = function(event) {
		if (validateForm()) {
			var createRequest = new XMLHttpRequest();
		
			var form = document.getElementById('createAccountForm');
			var formData = new FormData(form);
			
			createRequest.open('POST', url, true);
			createRequest.addEventListener('load', function() {
				if (createRequest.status >= 200 && createRequest.status < 400) {
					var response = JSON.parse(createRequest.responseText);
					dialogSpawn("Result",response.message,"resultBox","resultTitle","resultInfo");
					//document.getElementById('registerResult').textContent = response.message;
					//Check for substring in response indicating successful account creation
					//Change color of response message to green if found
					/*if (response.message.indexOf("success") != -1) {
						document.getElementById('registerResult').style.color = "green";
					}*/
				} else {
					//document.getElementById('registerResult').textContent = "Server is unreachable at this time";
					dialogSpawn("Error","Server is unreachable at this time","resultBox","resultTitle","resultInfo");
				}
			});

			createRequest.send(formData);
			event.preventDefault();
		}
		else {
			//document.getElementById('registerResult').textContent = "You must fill out all fields and upload a file.";
			dialogSpawn("Error","You must fill out all fields and upload a file.","resultBox","resultTitle","resultInfo");
		}
	}
}

function validateForm() {
	var email = document.getElementsByName("email")[0].value;
	var fName = document.getElementsByName("firstName")[0].value;
	var lName = document.getElementsByName("lastName")[0].value;
	var password = document.getElementsByName("password")[0].value;
	var file = document.getElementsByName("signatureFile")[0].value;

	if (email == null || email == "" || fName == null || fName == "" 
		|| lName == null || lName == "" || password == null || file == "") {
		return false;
	}
	return true;
}
