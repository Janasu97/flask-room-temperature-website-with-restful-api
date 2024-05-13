// Function to display a dialog box with message and options
function showDialog(message, callback) {
    const dialogBox = document.createElement('div');
    dialogBox.classList.add('dialog-box');

    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    dialogBox.appendChild(messageElement);

    const buttonContainer = document.createElement('div'); // Create a container for buttons
    buttonContainer.classList.add('button-container');

    const okButton = document.createElement('button');
    okButton.textContent = 'Ok';
    okButton.classList.add('ok-button');
    okButton.addEventListener('click', () => {
        hideDialog();
        if (callback) callback(true);
    });
    buttonContainer.appendChild(okButton); // Append the Ok button to the container

    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancel';
    cancelButton.classList.add('cancel-button');
    cancelButton.addEventListener('click', () => {
        hideDialog();
        if (callback) callback(false);
    });
    buttonContainer.appendChild(cancelButton); // Append the Cancel button to the container

    dialogBox.appendChild(buttonContainer); // Append the button container to the dialog box

    document.body.appendChild(dialogBox);
}

// Function to hide the dialog box
function hideDialog() {
    const dialogBox = document.querySelector('.dialog-box');
    if (dialogBox) {
        dialogBox.parentNode.removeChild(dialogBox);
    }
}
