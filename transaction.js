document.addEventListener("DOMContentLoaded", function() {
    // Select all cells with the "reputation" class
    const reputationCells = document.querySelectorAll('.rep');

    reputationCells.forEach(cell => {
        const repValue = parseInt(cell.getAttribute('data-rep'), 10); // Get the reputation value from data-rep attribute
        let stars = '';
        for (let i = 0; i < repValue; i++) {
            stars += '★ '; // Append a star for each point in reputation
        }
        cell.textContent = stars; // Set the cell text to the stars string
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const statusCells = document.querySelectorAll('.status');

    statusCells.forEach(divElement => {
        const spanElement = divElement.querySelector('p'); // Find the span inside the div
        const value = spanElement.textContent.trim(); // Get the text content of the span

        if (value === '1') {
            divElement.classList.add('green');
            spanElement.textContent = "Available"; // Set the text inside the span
        } else if (value === '0') {
            divElement.classList.add('red');
            spanElement.textContent = "Not Available"; // Set the text inside the span
        } else {
            divElement.classList.add('orange');
            spanElement.textContent = "Unknown"; // Set the text inside the span
        }
    });
});
