// global variable that stores the table data
// modified everytime a new query runs
var queryData = null;

// makes the element visible
function spawn(idVal) {
	var form = document.getElementById(idVal);
	form.style.display="block";
}

// makes the element not visible
function deSpawn(idVal) {
	var form = document.getElementById(idVal);
	form.style.display="none";
}

/*
 * JS code that sends the fields/filter options, based on user input, in JSON form via a POST request to ~/filterData
 * filterReq is called when the filter form is submitted on admin_dashboard.html
 */ 

var url = '../filterData';

function filterReq() {

    var data={}; // initialize dictionary
    var fTable = document.getElementById("filterDataTable"); // get the table

    var headers = [];

    var fields = document.getElementsByClassName("fields");
    for (var i=0,y=0; i<fields.length;i++) {
        if (fields[i].checked) {
            // use a switch statement to determine the header content
            // push the header names to the headers array
            switch (fields[i].value) {
                case "type":
                    headers.push("Award Type");
                    break;
                case "awardee":
                    headers.push("Awardee Name");
                    break;
                case "email":
                    headers.push("Awardee Email");
                    break;
                case "dateAwarded":
                    headers.push("Date Created");
                    break;
                case "userId":
                    headers.push("User ID");
                    break;
                case "userName":
                    headers.push("User Full Name");
                    break;
                default:
                    console.log("Error printing out table header");
            }
              data["option"+y] = fields[i].value; // set dictionary value
            y++;
        }
    }

    // if y==0, then no headers were selected 
    // show error in a notification and return
    var errMess = "Please make sure you select at least 1 field before proceeding. If you selected a filter, please make sure you entered a value to filter by.";
    if (y==0) {
        dialogSpawn("Error",errMess,"notif","errTitle","filterText");
        return;
    }

    // get the filter values
    data["filter"] = document.getElementById("filters").value;
    data["filterVal"] = document.getElementById("filterVal").value;
    

    // if a filter option is provided but no filter value is provided, then alert the user and return
    if (data["filter"] != "none" && data["filterVal"] == "") {
        dialogSpawn("Error",errMess,"notif","errTitle","filterText");
        return;
    }

    // once this point is reached, the filter options are accepted
    deSpawn('filterMenu'); // close the window

    // clear the table and add in the headers
    // header titles are stored in the headers array
    fTable.innerHTML="";
    var header = fTable.createTHead();
    var rowHeader = header.insertRow();
    var thCell;
    for (var t=0; t<headers.length; t++) {
//        rowHeader.insertCell(t).innerHTML = headers[t];
        thCell = document.createElement("th");
        thCell.appendChild(document.createTextNode(headers[t]));
        rowHeader.appendChild(thCell);
    }

    data["size"] = y;

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
            queryData = [];
            queryData.push(headers); // push header array into queryData       
            // display the results in the table
        //   var footer = fTable.createTFoot();
           var newRow, temp, headerCell;
           for (var c=0;c<response.length;c++) {
                queryData.push(response[c]); // push array into queryData global variable
                newRow = header.insertRow(c+1); // insert a new row
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


/**
 * Take the data current stored in the global variable - queryData (if it is not null)
 * Convert data to CSV format and then have it download on the client's computer
 **/ 
function exportCSV() {

    if (queryData != null && queryData != "") {
        console.log(queryData);
    } else {
        // let user know there is an error
        dialogSpawn("Error","Please query data before exporting to a CSV file.","notif","errTitle","filterText");
        return;
    }

    var temp, csvStr = ""; // set csvStr to an empty string
    // concat csvStr together to form a string in CSV format
    // values on the same line are separated by commas, values on different lines are separated by newline character
    for (var a=0; a<queryData.length; a++) {
        temp = queryData[a];
        for (var b=0; b<temp.length; b++) {
            if (b < temp.length-1)
                csvStr = csvStr + temp[b] + ",";
            else
                csvStr = csvStr + temp[b] + "\n";
        }
    }


    /**
     * References for CSV exporting code:
     * http://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side (Oliver Lloyd's edit reponse)
     * http://stackoverflow.com/questions/17836273/export-javascript-data-to-csv-file-without-server-interaction (adeneo's response)
     **/ 

    // encode csvStr - escapes certain characters
    var encodedStr = encodeURI(csvStr);
    console.log(encodedStr);
    var downloadLnk = document.createElement("a");
    downloadLnk.setAttribute("href",'data:attachment/csv,'+encodedStr);
    downloadLnk.setAttribute("download","awards_data.csv");
    document.body.appendChild(downloadLnk); 

    downloadLnk.click();
}
