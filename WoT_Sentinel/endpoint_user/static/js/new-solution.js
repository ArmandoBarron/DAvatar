var form = document.forms.namedItem("myform");
form.addEventListener('submit', function(ev) {

  var oOutput = document.getElementById("form-response");
  oData = new FormData(form);

  // append extra data
  oData.append("monitor_interval", document.getElementById("monitor_interval").value);
  oData.append("aggregates_interval", document.getElementById("aggregates_interval").value);

  var oReq = new XMLHttpRequest();
  oReq.open("POST", "/upload-file", true);
  oReq.onload = function(oEvent) {
    if (oReq.status == 200) {
      oOutput.innerHTML = "Uploaded!";
    } else {
      oOutput.innerHTML = "Error " + oReq.status + " occurred when trying to upload your file.<br \/>";
    }
  };

  oReq.send(oData);
  ev.preventDefault();
}, false);