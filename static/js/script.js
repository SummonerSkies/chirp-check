// ADDING BIRD TO EXISTING CHECKLIST

// // Function to toggle the bird status between "Spotted" and "Not Seen"
// function toggleStatus(birdId) {
//     const statusText = document.getElementById(`status-text-${birdId}`);
//     const countInput = document.getElementById(`count-input-${birdId}`);
//     const numberSeenDiv = document.getElementById(`number-seen-${birdId}`);
//     const toggleButton = document.getElementById(`toggle-btn-${birdId}`);

//     // Toggle status: If it's "Spotted", mark it as "Not Seen", and vice versa
//     if (statusText.innerText === "Spotted") {
//         // Change status to "Not Seen"
//         statusText.innerText = "Not Seen";
//         numberSeenDiv.style.display = "none";  // Hide number seen field
//         countInput.disabled = true;  // Disable input field
//         toggleButton.innerText = "Mark as Spotted";  // Change button text
//     } else {
//         // Change status to "Spotted"
//         statusText.innerText = "Spotted";
//         numberSeenDiv.style.display = "block";  // Show number seen field
//         countInput.disabled = false;  // Enable input field
//         toggleButton.innerText = "Mark as Not Seen";  // Change button text
//     }
// }

// // Event listener for the toggle status button
// document.querySelectorAll('.toggle-status-btn').forEach(button => {
//     button.addEventListener('click', function(event) {
//         const birdId = event.target.id.split('-')[2]; // Extract bird ID from the button's ID
//         toggleStatus(birdId);
//     });
// });
