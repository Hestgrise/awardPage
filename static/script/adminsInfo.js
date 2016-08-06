console.log("Account info populating JavaScript is working")
document.addEventListener('DOMContentLoaded', pageLoad);
var url = '../adminsInfo';
var deleteUrl = '../deleteAdminAccount';
var editUrl = '../editAdminAccount';

function pageLoad() {
	var createRequest = new XMLHttpRequest();

	createRequest.open('POST', url, true);
	createRequest.setRequestHeader('Content-Type', 'application/json');
	createRequest.addEventListener('load', function() {
		if (createRequest.status >= 200 && createRequest.status < 400) {
			var response = JSON.parse(createRequest.responseText);
			var table = document.getElementById("adminsTable")
			var numAdmins = response.emails.length;
			for (var i = 0; i < numAdmins; i++) {
				var row = table.insertRow(i + 1);
				var editRadio = document.createElement("input");
				editRadio.setAttribute("type", "radio");
				editRadio.setAttribute("value", response.ids[i]);
				editRadio.setAttribute("name", "toEdit");
				var deleteBtn = document.createElement("input");
				deleteBtn.setAttribute("type", "checkbox")
				deleteBtn.setAttribute("value", response.ids[i]);
				deleteBtn.setAttribute("name", "toDelete");
				var checkBoxCell = row.insertCell(0);
				var radioCell = row.insertCell(1);
				checkBoxCell.appendChild(deleteBtn);
				radioCell.appendChild(editRadio)
				row.insertCell(2).innerHTML = response.emails[i];
				row.insertCell(3).innerHTML = response.dates[i];
			}
		}
		else {
			document.getElementById('result').textContent = "Server is unreachable at this time";
		}
	});

	createRequest.send();
	event.preventDefault();

	var deleteButton = document.getElementById("deleteAdminsBtn");

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

	var editButton = document.getElementById("editAdminBtn");
	editButton.onclick = function(event) {
		editRequest = new XMLHttpRequest();

	};
}