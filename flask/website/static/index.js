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

function closeQuestionPopup() {
    // Remove the overlay and modal container from the document
    const overlay = document.querySelector('.overlay');
    const modalContainer = document.querySelector('.modal-container');

    if (overlay && modalContainer) {
        document.body.removeChild(overlay);
        document.body.removeChild(modalContainer);
    }
}


function submitAnswer() {
    // Handle answer submission logic here
    // You can modify this function to check the selected answer and update points accordingly
    // After handling the answer, close the modal
    closeQuestionPopup();
}

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function () {
    const questionButtons = document.querySelectorAll('.question-button');

    function openQuestionPopup(category, value) {
        fetch(`/get_question/${category}/${value}`)
            .then(response => response.json())
            .then(data => {
                // Create an HTML document with the question and answer choices
                const modalContent = `
                    <div class="question-container">
                        <div id="question-text" class="question-text">${data.question_text}</div>
                        <ul id="answer-choices" class="answer-choices">
                            ${data.answer_choices.map(choice => `<li>${choice}</li>`).join('')}
                        </ul>
                        <button onclick="submitAnswer()">Submit Answer</button>
                        <button onclick="closeQuestionPopup()">Close</button>
                    </div>
                `;

                // Display the modal with the question content
                showModal(modalContent);
            })
            .catch(error => console.error('Error fetching question:', error));
    }

    function showModal(content) {
        // Create and append the overlay div
        const overlay = document.createElement('div');
        overlay.classList.add('overlay');
        document.body.appendChild(overlay);
    
        // Create and append the modal container
        const modalContainer = document.createElement('div');
        modalContainer.classList.add('modal-container');
        modalContainer.innerHTML = content;
        document.body.appendChild(modalContainer);
    }

    questionButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const category = button.getAttribute('data-category');
            const pointValue = button.getAttribute('data-point-value');

            openQuestionPopup(category, pointValue);
        });
    });
});
