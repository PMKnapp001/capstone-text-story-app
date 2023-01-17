function displayForm(formId) {
    if (formId == 'create') {
        document.querySelector('#create-account').style.display = "";
        document.querySelector('#login-account').style.display = "none";
    }
    else {
        document.querySelector('#login-account').style.display = "";
        document.querySelector('#create-account').style.display = "none";
    }
}

const accountToggles = document.querySelectorAll('.account-toggle');

for (const toggle of accountToggles) {
    toggle.addEventListener('click', (evt) => {
        evt.preventDefault();
        
        displayForm(toggle.id);

    });
}