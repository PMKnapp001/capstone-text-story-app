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
                    resultsContainer.style.display = ''
                    resultsContainer.insertAdjacentHTML('beforeend', `<h3>Results:</h3>`);
                    console.log(responseData)
                    if (userOrStory == 'user') {
                        if (Object.keys(responseData).length === 0){
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<li class="list-group-item border border-dark story-item-background result-link">No usernames found!</li>`);
                        }
                        for (const result of Object.keys(responseData)) {
                            
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<li class="list-group-item border border-dark story-item-background result-link"><a href="/users/${responseData[result]['user_id']}/profile">${responseData[result]['username']}</a></li>`);
                        }
                    }

                    else {
                        if (Object.keys(responseData).length === 0){
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<li class="list-group-item border border-dark story-item-background result-link">No stories found!</li>`);
                        }
                        for (const result of Object.keys(responseData)) {
                            
                            resultsContainer.insertAdjacentHTML('beforeend',
                                `<ul id="${responseData[result]['story_id']}" class="list-group border-dark list-group-horizontal mb-3 text-center">
                                <a class="list-group-item story-item-background border-dark flex-fill"> 
                                    <div class="d-flex w-100 justify-content-between">
                                        <h4 class="mb-1 text-decoration-underline">${responseData[result]['title']}</h5>
                                    </div>
                                    <p class="mb-1">${responseData[result]['synopsis']}</p>
                                    <small class="text-muted">Average Rating: ${responseData[result]['rating']}</small>                              
                                </a>
                                <a href="/user/${responseData[result]['user_id']}/stories/${responseData[result]['story_id']}" class="border-dark list-group-item text-bg-primary pt-4">
                                    <div>
                                        <i class="bi bi-book-fill" style="font-size: 2rem;"></i>
                                    </div>
                                    Play
                                </a>
                            </ul>`);
                                
                        }
                    }         
                });
        }
    }

});


