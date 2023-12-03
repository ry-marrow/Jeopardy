// Define a variable to track the dollar total
let dollarTotal = 0;

// Function to update the dollar total and display it
function updateDollarTotal(amount, isIncrement = true) {
    console.log(Number(amount));
    if (isIncrement) {
        // Increment the dollar total
        dollarTotal += Number(amount);
    } else {
        // Decrement the dollar total
        dollarTotal -= Number(amount);
    }

    // Update the displayed total in the HTML
    const totalDisplay = document.getElementById('dollar-total');
    totalDisplay.textContent = `${dollarTotal}`; // Update the content
}

function closeQuestionPopup() {
    clearInterval(timerInterval);
    // Remove the overlay and modal container from the document
    const overlay = document.querySelector('.overlay');
    const modalContainer = document.querySelector('.modal-container');

    if (overlay && modalContainer) {
        document.body.removeChild(overlay);
        document.body.removeChild(modalContainer);
    }
}


function submitAnswer() {
    // Get the selected answer
    const selectedAnswer = document.querySelector('.answer-choices button.selected');

    if (selectedAnswer) {
        // Get the category, value, and correctness
        const category = selectedAnswer.getAttribute('data-category');
        const value = selectedAnswer.getAttribute('data-point-value');
        const isCorrect = selectedAnswer.textContent === correctAnswer; // Compare with correct answer

        // Assuming your server expects a POST request with JSON data
        fetch('/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                category: category,
                value: value,
                isCorrect: isCorrect,
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Update player's total based on the response from the server
            if (data.playerIndex !== undefined && data.points !== undefined) {
                updatePlayerTotal(data.playerIndex, data.points);
            }
        })
        .catch(error => console.error('Error submitting answer:', error))
        .finally(() => {
            // Close the modal after handling the answer
            closeQuestionPopup();
        });
    } else {
        console.error('No answer selected.');
        // You might want to display a message to the user indicating that they need to select an answer.
    }
}

function closeAlert() {
    var alert = document.querySelector(".alert");
    alert.style.display = "none";
}

function selectAnswer(button, pointValue, correctAnswer) {
    // Deselect any previously selected answers
    const selectedAnswers = document.querySelectorAll('.answer-choices button.selected');
    
    console.log('answer selected!!!!!!', pointValue)
    selectedAnswers.forEach(answer => answer.classList.remove('selected'));

    // Select the clicked answer
    button.classList.add('selected');
    // Check if the selected answer is correct
    const selectedText = button.textContent;
    const isCorrect = selectedText === correctAnswer;

    // Display a message to the user based on correctness
    const resultMessage = isCorrect ? 'Correct! Score Increased.' : 'Incorrect. Score decreased.';

    // Create a new element for the result message
    // const resultElement = document.createElement('div');
    // resultElement.classList.add('result-message');
    // resultElement.textContent = resultMessage;

    // Update the modal content with the result message
    const modalContent = document.querySelector('.modal-container .question-container');
    modalContent.innerHTML = `
        <div class="question-text">${resultMessage}</div>
        <div class="point-value">Point Value: ${pointValue}</div>
    `;

    // Append the result message to the modal content
    //modalContent.appendChild(resultElement);

    // Logic based on the selected answer
    if (isCorrect) {
        console.log('Correct answer!');
        
        // Increment the dollar value total for the player
        updateDollarTotal(pointValue);
    } else {
        console.log('Incorrect answer!');
        
        // Decrement the dollar value total for the player
        updateDollarTotal(pointValue, false);
    }

    setTimeout(() => {
        closeQuestionPopup(); // Close the current modal
    }, 5000);
}


// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function () {
    const questionButtons = document.querySelectorAll('.question-button');

    function openQuestionPopup(category, value) {
        console.log('value', value);
        fetch(`/get_question/${category}/${value}`)
            .then(response => response.json())
            .then(data => {
                // Assuming your server sends the correct answer as part of the response
                const correctAnswer = data.correct_answer;

                // Create an HTML document with the question and answer choices
                const modalContent = `
                    <div class="question-container">
                        <div id="question-text" class="question-text">${data.question_text}</div>
                        <div id="answer-choices" class="answer-choices">
                            ${data.answer_choices.map(choice => `<button class="options" data-point-value="${value}" onclick="selectAnswer(this, ${value})">${choice}</button>`).join('')}                        </div>
                        <div class="timer-container">
                            <div id="timer" class="timer">15</div>
                        </div>
                    </div>
                `;

                // Display the modal with the question content
                showModal(modalContent);

                // Attach the selectAnswer function directly to each answer button
                // const answerButtons = document.querySelectorAll('.answer-choices button');
                // answerButtons.forEach(button => {
                //     button.addEventListener('click', function () {
                //         selectAnswer(button, value, correctAnswer);
                //     });
                // });

                // Start the 15-second timer
                let timerSeconds = 15;
                const timerDisplay = document.getElementById('timer');

                timerInterval = setInterval(function () {
                    timerDisplay.textContent = timerSeconds;
                    timerSeconds--;

                    if (timerSeconds < 0) {
                        clearInterval(timerInterval);
                        // Time is up, close the modal
                        closeQuestionPopup();
                    }
                }, 1000);
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
