// ADDING BIRD TO EXISTING CHECKLIST

// Function to toggle visibility of the "Number Seen" input based on the status
function toggleNumberSeen(birdId) {
    var statusSelect = document.getElementById('status_' + birdId);
    var numberSeenDiv = document.getElementById('number_seen_' + birdId);
    var numberSeenInput = document.getElementById('number_seen_input_' + birdId);

    // Show or hide the 'Number Seen' field based on status
    if (statusSelect.value === "Spotted") {
        numberSeenDiv.style.display = "block";  // Show the field
        numberSeenInput.disabled = false;      // Enable the input
    } else {
        numberSeenDiv.style.display = "none";   // Hide the field
        numberSeenInput.disabled = true;       // Disable the input
    }
}

// Ensure that each bird's status field is correctly initialized when the page loads
document.addEventListener("DOMContentLoaded", function() {
    var allStatusSelects = document.querySelectorAll('.status-select');
    allStatusSelects.forEach(function(select) {
        var birdId = select.id.split('_')[1]; // Extract bird ID from the select element's ID
        toggleNumberSeen(birdId);  // Initialize the visibility based on current status
    });
});