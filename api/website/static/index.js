// function deleteNote(noteId){
//     fetch('/delete-note', {
//         method: 'POST',
//         body: JSON.stringify({noteId:noteId})
//     }).then((_res) => {
//         window.location.href = "/"  //refresh the page
//     });
// }

function closeAlert() {
    var alert = document.querySelector(".alert");
    alert.style.display = "none";
}
  


// Define a variable to track the dollar total
let dollarTotal = 0;

// Function to update the dollar total and display it
function updateDollarTotal(increment) {
    dollarTotal += increment;
    // Update the displayed total in the HTML
    const totalDisplay = document.getElementById('dollar-total');
    totalDisplay.textContent = dollarTotal; // Update the content

    // Add the dollar sign and formatting
    const formattedTotal = dollarTotal;
    totalDisplay.textContent = formattedTotal;
}

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the popup and iframe
    const questionPopup = document.getElementById('question-popup');
    const questionIframe = document.getElementById('question-iframe');
    const cells = document.querySelectorAll('.question-trigger');

    let point_value = 0; // Initialize the point_value variable

    // Add a click event listener to each gameboard cell
    cells.forEach(function(cell) {
        cell.addEventListener('click', function(event) {
            event.preventDefault();

            // Get the category_id and point_value from data attributes
            const category_id = this.getAttribute('data-category-id');
            point_value = this.getAttribute('data-point-value'); // Update point_value

            // Set the iframe source to the question route
            questionIframe.src = `/question/${category_id}/${point_value}/options`;

            // Show the question popup
            questionPopup.style.display = 'block';
        });
    });

    // Function to receive messages from the iframe
    function receiveMessage(event) {
        if (event.data && event.data.answer) {
            const answer = event.data.answer;
            const correctAnswer = "A. Python"; // Update with the actual correct answer

            if (answer === correctAnswer) {
                // Increment the dollar total by the question's point value
                updateDollarTotal(parseInt(point_value));
                alert("Correct answer! Your total is now $" + dollarTotal);
            } else {
                // Handle incorrect answers here (if needed)
                alert("Incorrect answer. Try again.");
            }

            // Close the popup
            questionPopup.style.display = 'none';
        }
    }

    // Listen for messages from the iframe
    window.addEventListener('message', receiveMessage, false);
});


/*=============== SHOW HIDDEN - PASSWORD ===============*/
const showHiddenPass = (loginPass, loginEye) =>{
    const input = document.getElementById(loginPass),
          iconEye = document.getElementById(loginEye)
 
    iconEye.addEventListener('click', () =>{
       // Change password to text
       if(input.type === 'password'){
          // Switch to text
          input.type = 'text'
 
          // Icon change
          iconEye.classList.add('ri-eye-line')
          iconEye.classList.remove('ri-eye-off-line')
       } else{
          // Change to password
          input.type = 'password'
 
          // Icon change
          iconEye.classList.remove('ri-eye-line')
          iconEye.classList.add('ri-eye-off-line')
       }
    })
 }
 
 showHiddenPass('login-pass','login-eye')