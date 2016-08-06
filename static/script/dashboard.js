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
		//event.preventDefault();
	};
	//We call the function to fill in the awards defined just above
	showAwards();
	
	var submitButton = document.getElementById('certSubmit');
	submitButton.onclick = function(event)
	{

		var forgotReq = new XMLHttpRequest();
		
		var userInfo = {empName:document.getElementById("fullName").value,
						empEmail:document.getElementById("email").value,
						awdType:document.getElementById("awardType").value,
						dateAwarded:document.getElementById("dateAwarded").value
						};
		//console.log(str(userInfo(dateAwarded)));
		var payLoad = JSON.stringify(userInfo);
		
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
			
		});
		
		forgotReq.send(payLoad);
		event.preventDefault();
		
	}
	
}
