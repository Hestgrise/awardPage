console.log("Account info populating JavaScript is working")
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../recentAwards'
//Credit for some asistance with JavaScript code implementation to Professor Wolford CS 290 Lectures 
function pageLoad() {
	var createRequest = new XMLHttpRequest();

	createRequest.open('POST', url, true);
	createRequest.setRequestHeader('Content-Type', 'application/json');
	createRequest.addEventListener('load', function() {
		if (createRequest.status >= 200 && createRequest.status < 400) {
			var response = JSON.parse(createRequest.responseText);
			document.getElementById("accountName").innerHTML = response.accountName;
			document.getElementById("accountEmail").innerHTML = response.accountEmail;
			document.getElementById("accountDate").innerHTML = response.accountDate;
			document.getElementById("accountAwards").innerHTML = response.accountAwards;
			document.getElementById("result").style.color = "green";
			document.getElementById("result").innerHTML = "Account information is up to date." 
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send();
	event.preventDefault();
}