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
