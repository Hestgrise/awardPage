



console.log("Javascript is working");
document.addEventListener('DOMContentLoaded', buttonSet);


function buttonSet()
{
	var submitButton = document.getElementById('forgetSubmitButton');
	
	submitButton.onclick = function(event)
	{

		var forgotReq = new XMLHttpRequest();
		
		var userInfo = {fEmail:document.getElementById("fEmail").value};
		
		var payLoad = JSON.stringify(userInfo);
		
		forgotReq.open('POST', 'http://127.0.0.1:5432/passTest', true);
		
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