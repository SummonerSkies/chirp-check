// ADDING BIRD TO EXISTING CHECKLIST

// Function to toggle visibility of the "Number Seen" input based on the status
function toggleStatus(birdId) {
    const statusSpan = document.getElementById('status-' + birdId);
    const countDiv = document.getElementById('number-seen-' + birdId);
    const countInput = document.getElementById('count-input-' + birdId);
    const status = statusSpan.querySelector('span');
    
    // Toggle the status between "Spotted" and "Not Seen"
    if (status.classList.contains('not-seen')) {
        // Change to "Spotted"
        status.classList.remove('not-seen');
        status.classList.add('spotted');
        status.innerText = 'Spotted';

        // Show the number_seen input
        countDiv.style.display = 'block';
    } else {
        // Change to "Not Seen"
        status.classList.remove('spotted');
        status.classList.add('not-seen');
        status.innerText = 'Not Seen';

        // Hide the number_seen input
        countDiv.style.display = 'none';
        countInput.value = 0;  // Reset count
    }
}