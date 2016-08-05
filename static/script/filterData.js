/*
 * JS code that builds queries based on user input and then sends them via a POST request to ~/filterData
 */ 

var url = '../filterData' // URL that receives the POST request

function filterReq() {


    despawn(); // first call despawn to close the window
//    var request = new XMLHttpRequest(); // initialize a new HTTP request

    /**
     * Troy's response provided code assistance with getting data from checkboxes via javascript
     * http://stackoverflow.com/questions/20649146/using-document-getelementsbyclass-with-checkboxes
     **/ 
    var fields = document.getElementsByClassName("fields");
    var header = fields.createTHead();
    var rowHeader = header.insertRow();
    var fTable = document.getElementById("filterDataTable");
    for (var i=0,y=0; i<fields.length; i++) {
        if (fields[i].checked) {
            rowHeader.insertCell(y).innerHTML=fields[i].value;
            y=0;
    }


}

