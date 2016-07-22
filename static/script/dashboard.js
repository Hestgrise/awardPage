



console.log("Javascript is working");
document.addEventListener('DOMContentLoaded', buttonSet);


function buttonSet()
{
	var submitButton = document.getElementById('certSubmit');
	
	submitButton.onclick = function(event)
	{

		var forgotReq = new XMLHttpRequest();
		
		var userInfo = {empName:document.getElementById("fullName").value,
						empEmail:document.getElementById("email").value,
						awdType:document.getElementById("awardType").value
						};
		
		var payLoad = JSON.stringify(userInfo);
		
		forgotReq.open('POST', '../createAward', true);
		
		forgotReq.setRequestHeader('Content-Type', 'application/json');
		
		forgotReq.addEventListener('load', function()
		{
			if(forgotReq.status >= 200 && forgotReq.status < 400)
			{
				var response = JSON.parse(forgotReq.responseText);
				document.getElementById('result').textContent = response.message;
				
			}
			else
			{
				document.getElementById('result').textContent = "Server is unreachable at this time";
			}
			
			
			
		});
		
		forgotReq.send(payLoad);
		event.preventDefault();
		
	}
	
}