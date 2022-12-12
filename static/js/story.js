function turnButtonsOff(previousButtonId) {
    const allButtonUl = document.querySelectorAll('.branch-prev');
    for (const buttonUl of allButtonUl) {
        if (buttonUl.id != previousButtonId) {
            buttonUl.style.display = 'none';
        }

        else {
            buttonUl.style.display = '';
        }
    } 
}


const choiceButtons = document.querySelectorAll('.branch-choice');
turnButtonsOff("1");

for (const button of choiceButtons) {
    button.addEventListener('click', (evt) => {
        evt.preventDefault();

        turnButtonsOff(button.value);
        const clickedBranchId = button.value;

        fetch(`/api/branch?branch_id=${clickedBranchId}`)
            .then((response) => response.json())
            .then((responseData) => {
                let buttonContainer = document.querySelector('#buttons-div');
                

                buttonContainer.insertAdjacentHTML('beforebegin',
                    `<div class="branch-body">${responseData['body']}</div>`);
                buttonContainer.insertAdjacentHTML('beforebegin',
                    `<div class="branch-prompt">${responseData['branch_prompt']}</div>`);
                
            });
    });
}
