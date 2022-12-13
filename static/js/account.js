function displayForm(formButtonId) {
    if (formButtonId == 'create') {
        document.querySelector('#create-account').style.display = ""
    }
    else {
        document.querySelector('#login-account').style.display = ""
    }
}

function turnOffAccountButtons() {
    const accountButtons = document.querySelectorAll('.account-buttons');
    for (const button of accountButtons) {
        button.style.display = 'none'
    }
}

const accountButtons = document.querySelectorAll('.account-buttons');

for (const button of accountButtons) {
    button.addEventListener('click', (evt) => {
        evt.preventDefault();

        turnOffAccountButtons();
        displayForm(button.id)

    });
}