var myVar = setInterval(function() {
  myTimer();
});

function myTimer() {
  var d = new Date();
  document.getElementById("time").innerHTML = d.toLocaleTimeString();
}
