console.log("Javascript is working");
document.addEventListener('DOMContentLoaded', pageLoad);

function pageLoad()
{


	function showAwards(event)	{
		
		//First we remove any awards that are present
		oldAwards = document.getElementById('recentAwardsList');
		while(oldAwards.firstChild){
			oldAwards.removeChild(oldAwards.firstChild);
		}
		var createReq = new XMLHttpRequest();

		createReq.open('POST', '../recentAwards', true);
		createReq.setRequestHeader('Content-Type', 'application/json');
		createReq.addEventListener('load', function() {
			if (createReq.status >= 200 && createReq.status < 400) {
				var response = JSON.parse(createReq.responseText);
				var list = document.getElementById("recentAwardsList")
				var numAwards = response.names.length;
				for (var i = 0; i < numAwards; i++) {
					var li = document.createElement("li");
					var name = String(response.names[i]);
					var award = String(response.awards[i]);
					var date = String(response.dates[i]);
					var textNode = name + " was awarded " + award + " on " + date;
					li.appendChild(document.createTextNode(textNode));
					list.appendChild(li);
				}
			}
			else {
                // make dialog appear to show error
				dialogSpawn("Error","Server is unreachable at this time","resultBox","resultTitle","resultInfo");
			}
		});

		createReq.send();
		
	};
	//We call the function to fill in the awards defined just above
	showAwards();
	
	var submitButton = document.getElementById('certSubmit');
	submitButton.onclick = function(event)
	{
		submitButton.disabled = true;
		//submitButton.bgcolor='#ffffff';
		var validInput = true;
		var forgotReq = new XMLHttpRequest();
		
		var userInfo = {empName:document.getElementById("fullName").value,
						empEmail:document.getElementById("email").value,
						awdType:document.getElementById("awardType").value,
						dateAwarded:document.getElementById("dateAwarded").value
						};
		if(document.getElementById("fullName").value.length == 0)
		{
			dialogSpawn("Error","You must enter a name","resultBox","resultTitle","resultInfo");
			validInput = false;
			submitButton.disabled = false;
			//console.log("Name tripped");
		}
		else if(document.getElementById("email").value.length == 0)
		{
			dialogSpawn("Error","You must enter an email","resultBox","resultTitle","resultInfo");
			validInput = false;
			submitButton.disabled = false;
		}
		else if(document.getElementById("dateAwarded").value.length == 0)
		{
			dialogSpawn("Error","You must enter an award date and time if you are using FireFox the format is nnnn-nn-nnTnn:nn","resultBox","resultTitle","resultInfo");
			validInput = false;
			submitButton.disabled = false;
		}
		else if(document.getElementById("dateAwarded").value.length > 0)	//If our date is there, we want to check for the right format
		{
			var copyOfDateString = document.getElementById("dateAwarded").value;
			var listOfDateParts = copyOfDateString.split("-");
			if(listOfDateParts[0].length != 4 || isNaN(listOfDateParts[0]))		//Our date is not four digits, we have an error
			{
				dialogSpawn("Error","You must enter an award date and time if you are using FireFox the format is nnnn-nn-nnTnn:nn","resultBox","resultTitle","resultInfo");
				validInput = false;
				submitButton.disabled = false;
				//console.log("Failing length or not number for first test length is: ");
				//console.log(listOfDateParts[0].length);
				//console.log(" isNaN: ");
				//console.log(isNaN(listOfDateParts[0]));
			}
			else if(listOfDateParts[1].length != 2 || isNaN(listOfDateParts[1]))
			{
				dialogSpawn("Error","You must enter an award date and time if you are using FireFox the format is nnnn-nn-nnTnn:nn","resultBox","resultTitle","resultInfo");
				validInput = false;
				submitButton.disabled = false;
				//console.log("Failing length or not number for second test");
			}
			else if(listOfDateParts[2].length != 8)
			{
				dialogSpawn("Error","You must enter an award date and time if you are using FireFox the format is nnnn-nn-nnTnn:nn","resultBox","resultTitle","resultInfo");
				validInput = false;
				submitButton.disabled = false;
				//console.log("Failing length or not number for third test");
				//console.log("Failing length or not number for third test length is: ");
				//console.log(listOfDateParts[2].length);
				//console.log(" isNaN: ");
				//console.log(isNaN(listOfDateParts[2]));
			}
			else
			{
				//This gets our year portion of our date into a integer
				var numYear = +listOfDateParts[0];
				if(numYear > 2500 || numYear < 1901)
				{
					console.log("Triggering date range");
					dialogSpawn("Error","The year entered must be between 1901 and 2500","resultBox","resultTitle","resultInfo");
					validInput = false;
					submitButton.disabled = false;
				}
				
			}
		}
		
		if(validInput)
		{
			//console.log(str(userInfo(dateAwarded)));
			var payLoad = JSON.stringify(userInfo);
			console.log("valid input, date was: " + userInfo['dateAwarded']);
			
			forgotReq.open('POST', '../createAward', true);
			
			forgotReq.setRequestHeader('Content-Type', 'application/json');
			
			forgotReq.addEventListener('load', function()
			{
				if(forgotReq.status >= 200 && forgotReq.status < 400)
				{
					var response = JSON.parse(forgotReq.responseText);
	//				document.getElementById('result').textContent = response.message;
					// call dialog to display results				
					dialogSpawn("Success",response.message,"resultBox","resultTitle","resultInfo");

				}
				else
				{
	//				document.getElementById('result').textContent = "Server is unreachable at this time";
	//				call dialog to display error
					dialogSpawn("Error","Server is unreachable at this time","resultBox","resultTitle","resultInfo");
				}
				
				showAwards();
				submitButton.disabled = false;
		});
		
		
		forgotReq.send(payLoad);
		}
		event.preventDefault();
		
	}
	
}
