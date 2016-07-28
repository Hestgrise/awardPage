console.log("Account info populating JavaScript is working")
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../existingInfo'

function pageLoad() {
	var createRequest = new XMLHttpRequest();

	createRequest.open('POST', url, true);
	createRequest.setRequestHeader('Content-Type', 'application/json');
	createRequest.addEventListener('load', function() {
		if (createRequest.status >= 200 && createRequest.status < 400) {
			var response = JSON.parse(createRequest.responseText);
			var table = document.getElementById("awardsTable")
			var numAwards = response.types.length;
			for (var i = 0; i < numAwards; i++) {
				var row = table.insertRow(i + 1);
				var radioBtn = document.createElement("input");
				radioBtn.setAttribute("type", "radio");
				radioBtn.setAttribute("id", response.ids[i]);
				var radioCell = row.insertCell(0);
				radioCell.appendChild(radioBtn);
				row.insertCell(1).innerHTML = response.dates[i];
				row.insertCell(2).innerHTML = response.winners[i];
				row.insertCell(3).innerHTML = response.types[i];
			}
			//document.getElementById("").innerHTML = ;
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send();
	event.preventDefault();
}