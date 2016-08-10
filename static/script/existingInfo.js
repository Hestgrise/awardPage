console.log("Account info populating JavaScript is working");
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../existingInfo';
var deleteUrl = '../deleteAwards';

function pageLoad(event) {
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
				radioBtn.setAttribute("type", "checkbox");
				radioBtn.setAttribute("value", response.ids[i]);
				radioBtn.setAttribute("name", "toDelete");
				var radioCell = row.insertCell(0);
				radioCell.appendChild(radioBtn);
				row.insertCell(1).innerHTML = response.dates[i];
				row.insertCell(2).innerHTML = response.types[i];
				row.insertCell(3).innerHTML = response.winners[i];
			}
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send();
	event.preventDefault();

	var deleteButton = document.getElementById("deleteBtn");

	deleteButton.onclick = function(event) {
		var createReq = new XMLHttpRequest();

		var toDelete = document.getElementsByName("toDelete");
		var deleteIds = [];
		for (var i = 0; i < toDelete.length; i++) {
			if (toDelete[i].checked) {
				deleteIds.push(toDelete[i].value);
			}
		}
		var jsonIds = {ids:deleteIds};
		var payload = JSON.stringify(jsonIds);
//console.log(payload);
		createReq.open('POST', deleteUrl, true);
		createReq.setRequestHeader('Content-Type', 'application/json');
		createReq.addEventListener('load', function() {
			if (createReq.status >= 200 && createReq.status < 400) {
				window.location.reload();
			}
			else {
				document.getElementById('deleteResult').textContent = "Server is unreachable at this time";
			}
		});

		createReq.send(payload);
		event.preventDefault();
	}
}
