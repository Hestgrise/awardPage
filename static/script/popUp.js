// makes the filter menu visible
function spawn() {
	var form = document.getElementById("filterMenu");
	form.style.display="block";
}

// makes the filter menu not visible
function deSpawn() {
	var form = document.getElementById("filterMenu");
	form.style.display="none";
}

/*
 * JS code that sends the fields/filter options, based on user input, in JSON form via a POST request to ~/filterData
 * filterReq is called when the filter form is submitted on admin_dashboard.html
 */ 

var url = '../filterData';

function filterReq() {

    // first close the filter menu
    deSpawn();

    var data={}; // initialize dictionary
    var fTable = document.getElementById("filterDataTable"); // get the table
    fTable.innerHTML="";

    var header = fTable.createTHead();
    var rowHeader = header.insertRow();

    var fields = document.getElementsByClassName("fields");
    for (var i=0,y=0; i<fields.length;i++) {
        if (fields[i].checked) {
            // use a switch statement to determine the header content
            switch (fields[i].value) {
                case "type":
                    rowHeader.insertCell(y).innerHTML="Award Type";
                    break;
                case "awardee":
                    rowHeader.insertCell(y).innerHTML="Awardee Name";
                    break;
                case "email":
                    rowHeader.insertCell(y).innerHTML="Awardee Email";
                    break;
                case "dateAwarded":
                    rowHeader.insertCell(y).innerHTML="Date Created";
                    break;
                case "userId":
                    rowHeader.insertCell(y).innerHTML="User ID";
                    break;
                case "userName":
                    rowHeader.insertCell(y).innerHTML="User Full Name";
                    break;
                default:
                    console.log("Error printing out table header");
            }
              data["option"+y] = fields[i].value; // set dictionary value
            y++;
        }
    }

    // if no fields are selected, then don't submit a HTTP POST request
    if (y==0) {
        // pop up to let user know to select options
        return;
    }

    data["size"] = y;

    // get filter option
    data["filter"] = document.getElementById("filters").value;    
    data["filterVal"] = document.getElementById("filterVal").value;    
    console.log(data);

    if (data["filterVal"] == "")
        console.log("nada");

    var filterData = JSON.stringify(data); // make into JSON format
    // data is now in dictionary format - send to python api.py
    var filterOptions = new XMLHttpRequest();
    filterOptions.open('POST',url,true);
    filterOptions.setRequestHeader('Content-Type','application/json');

/**
 * Reference for parsing JSON in Javascript:
 * http://www.w3schools.com/json/json_http.asp (Examples 1 & 2)
 **/

    // add event listener for when data is received
    filterOptions.addEventListener('load', function() {
        if (filterOptions.status >= 200 && filterOptions.status < 400) {
            var response = JSON.parse(filterOptions.responseText);
//            console.log(response.length);

            // display the results in the table
           var footer = fTable.createTFoot();
           var newRow, temp;
           for (var c=0;c<response.length;c++) {
                newRow = footer.insertRow(c); // insert a new row
                temp = response[c];
                for (var d=0;d<temp.length;d++) {
                    newRow.insertCell(d).innerHTML = temp[d];
                }
            }   
        } else {
            console.log("Data retrieval fail");
        }

    });

    filterOptions.send(filterData);

}


