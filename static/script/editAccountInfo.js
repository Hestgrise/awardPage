console.log("Account info populating JavaScript is working")
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../editAccountName'

function pageLoad() {
	var createRequest = new XMLHttpRequest();

	createRequest.open('POST', url, true);
	createRequest.setRequestHeader('Content-Type', 'application/json');
	createRequest.addEventListener('load', function() {
		if (createRequest.status >= 200 && createRequest.status < 400) {
			var response = JSON.parse(createRequest.responseText);
			document.getElementById("currentName").innerHTML = response.currentName;
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send();
	event.preventDefault();
}