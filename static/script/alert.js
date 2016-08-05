// make a dialog appear
// sets the title, blurb
function dialogSpawn(title,text,dialogID,titleID,blurbID) {
    var dialog = document.getElementById(dialogID);
    dialog.style.display = "block";

    var titleBlock = document.getElementById(titleID);
    titleBlock.innerHTML = title;

    var blurb = document.getElementById(blurbID);
    blurb.innerHTML = text;

}

// make a dialog disappear
function dialogDeSpawn(idVal) {
    var dialog = document.getElementById(idVal);
    dialog.style.display = "none";

}
