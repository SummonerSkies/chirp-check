// Message time limit for visibility
var message_ele = document.getElementById("msg");
setTimeout(function() {
  message_ele.style.display = "none";
}, 3000);


// Delete Bird script
document.addEventListener('DOMContentLoaded', function () {
    // Get the form element by its ID
    const deleteBirdForm = document.getElementById('deleteBirdForm');
    
    if (deleteBirdForm) {
        deleteBirdForm.onsubmit = function(event) {
            const confirmation = confirm("Are you sure you want to remove this bird?");
            if (!confirmation) {
                event.preventDefault();
            }
        }
    }
});