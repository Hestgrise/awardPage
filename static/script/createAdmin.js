console.log("Account creation validation JavaScript is working");
//document.addEventListener('DOMContentLoaded', buttonSet);
var url ='../createAdminAccount';
//Credit for some asistance with JavaScript code implementation to Professor Wolford CS 290 Lectures 
// when button is clicked, then createAdminAccount will execute
function createAdminAccount() {
	//var submitButton = document.getElementById('createAdminButton');

	//submitButton.onclick = function(event) {
		var createRequest = new XMLHttpRequest();
		
		var form = document.getElementById('createAccountForm');
		var formData = new FormData(form);
		
		createRequest.open('POST', url, true);
		createRequest.addEventListener('load', function() {
			if (createRequest.status >= 200 && createRequest.status < 400) {
				var response = JSON.parse(createRequest.responseText);
//				document.getElementById('registerResult').textContent = response.message;
				//Check for substring in response indicating successful account creation
				//Change color of response message to green if found
				if (response.message.indexOf("success") != -1) {
//					document.getElementById('registerResult').style.color = "green";
//					success message will appear letting the user know the account was successfully created
                    dialogSpawn("Success",response.message,"resultBox","resultTitle","resultInfo");
//                    window.location = '/admins.html';
				} else
                    dialogSpawn("Error","There was a problem creating the account","resultBox","resultTitle","resultInfo");
			} else {
                // let user know that there was an error in reaching the server
				dialogSpawn("Error","Server is unreachable at this time","resultBox","resultTitle","resultInfo");
			}
		});

		createRequest.send(formData);
//		event.preventDefault();
//	}
}
