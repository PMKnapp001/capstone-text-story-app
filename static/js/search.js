const searchButton = document.querySelector('#search-submit');

searchButton.addEventListener('click', (evt) => {
    evt.preventDefault();

    let searchOptions = document.getElementsByName('search-for');
    let searchText = document.querySelector('#search-text').value;

    for (const option of searchOptions) {

        if (option.checked) {

            let userOrStory = option.value;
            fetch(`/api/search?user_or_story=${userOrStory}&search_text=${searchText}`)
                .then((response) => response.json())
                .then((responseData) => {
                    let resultsContainer = document.querySelector('#results-container');
                    resultsContainer.innerHTML = "";
                    if (userOrStory == 'user') {
                        for (const result of Object.keys(responseData)) {
                            
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<li class="result-link"><a href="/users/${responseData[result]['user_id']}/profile">${responseData[result]['username']}</a></li>`);
                        } 
                    }

                    else {
                        for (const result of Object.keys(responseData)) {
                            
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<li class="result-link"><a href="/user/${responseData[result]['user_id']}/stories/${responseData[result]['story_id']}">${responseData[result]['title']}</a></li>`);
                        } 
                    }
                               
                });
        }
    }

});