console.log("Account info populating JavaScript is working")
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../fillAdminEditUserPage'
//Credit for some asistance with JavaScript code implementation to Professor Wolford CS 290 Lectures 
function pageLoad(event) {
	//Parse out the user's id from the url
	var currentUrl = window.location.href;
	var paramIndex = currentUrl.indexOf("=");
	var editId = currentUrl.substring(paramIndex + 1);

	var createRequest = new XMLHttpRequest();

	var jsonId = {editId:editId};
	var payload = JSON.stringify(jsonId);

	createRequest.open('POST', url, true);
	createRequest.setRequestHeader('Content-Type', 'application/json');
	createRequest.addEventListener('load', function() {
		if (createRequest.status >= 200 && createRequest.status < 400) {
			var response = JSON.parse(createRequest.responseText);
			document.getElementById("currentName").innerHTML = response.currentName;
			document.getElementById("currentEmail").innerHTML = response.currentEmail;
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send(payload);
	event.preventDefault();

	//Send new values to endpoint in api.py to apply updates in database
	var editButton = document.getElementById("editBtn");
	editButton.onclick = function(event) {
		var editRequest = new XMLHttpRequest();
		var newName = document.getElementById("newName").value;
		var newEmail = document.getElementById("newEmail").value;

		var data = {userId:editId, newName:newName, newEmail:newEmail};
		var payload = JSON.stringify(data)

		editRequest.open('POST', '/doAdminEditUser', true);
		editRequest.setRequestHeader('Content-Type', 'application/json');
		editRequest.addEventListener('load', function() {
			if (editRequest.status >= 200 && editRequest.status < 400) {
				window.location = "/users.html";
			}
			else {
				document.getElementById('result').textContent = "Server is unreachable at this time";
			}
		});

		editRequest.send(payload);
		event.preventDefault();
	}

}
