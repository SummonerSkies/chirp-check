// Message time limit for visibility
document.addEventListener("DOMContentLoaded", function() {
  var message_ele = document.getElementById("msg");
  if (message_ele) {
    setTimeout(function() {
      message_ele.style.display = "none";
    }, 3000);
  }
});