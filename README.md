# What hAPPens next?

An application for creating, sharing, and experiencing choice driven stories.

## Background

I have always enjoyed playing tabletop adventures games with friends where the best part is the story everyone creates while playing.

I want to simplify the concept and make it more approachable so that users can create and share their own stories with branching plots. This type of storytelling is not new; the Choose Your Own Adventure books were first published in the 1970's and are now published 
by [Chooseco LLC.](https://www.cyoa.com/). However, the goal of my application is give storytellers a platform to present their stories while giving the players a space to share their experiences.

## Tech stack

- **Database:** PostgreSQL
- **Backend:** Python 3
- **Frontend:** Web browser

### Dependencies

- Python packages:
  - SQLAlchemy ORM
  - Flask
  - Jinja
- APIs/external data sources:
  - User generated content saved to database
  - [Project Gutenberg](https://www.gutenberg.org/): used to access copyright free books.
- Browser/client-side dependencies:
  - Bootstrap

## Current Features
- Basic user account functions (creation, deletion, login, logout)
- Story creation 
    - Users are able to write choice driven stories
- Story Edit
    - Users are able to access previously written stories
      and edit or add story content
    - Users can delete story on any level (note: deleting a branch
      recursively deletes all descendants)
- Story playthrough
    - Users can playthrough stories by clicking on choices when prompted
- Automatic bookmarking
    - Bookmarks are automatically created or updated whenever
      a user clicks on a choice
    - Users are able to continue stories from last choice made
    - Users can reset bookmark to start story from the beginning
    - Once an end has been reached during playthrough, the story 
      is added to user's playthrough section for future rereading
      or resetting
- Rating implementation
    - Users can create or update a rating for a story 
      (a user can only have one rating per story)
    - Story ratings are counted and an average rating is generated
- Favorites
    - Users can favorite a story to have it easily accessible from 
      profile
    - Users can remove favorites
- Top ten popular stories
    - Top ten stories (by amount of rating)
- Search
    - Users can search for other users by username
    - Users can search for stories by title


## Future Updates
- password hashing
- Friends list implementation
- Story/Playthrough sharing via links, email, etc.
- User profile update
    - editing information
    - password recovery
- Comment implementation
- Basic animation

## Demo Build

- Current database build (seed-story-app-database.py) builds tables and
  creates the following records/objects:
    - Three users (TestUser1, TestUser2, TestUser3) with respective 
      passwords (TestPass1, TestPass2, TestPass3)
    - Five stories
        - each have intro branch with two children branches which each 
          have two children branches
        - One story by TestUser1, two by TestUser2, and two by TestUser3
        - Branch content is generated from markov chain generator (markov.py) 
          using clever-grethel.txt, rabbits-bride.txt, and six-soldiers-of-fortune.txt
          as input
    - Six ratings
        - Scores are random
        - Four ratings by TestUser1 for stories 2,3,4,5
        - Two by TestUser3 for stories 1, 2
    - Four favorites
        - Two by TestUser1 for stories 2 and 3
        - One by testUser2 for story 3
        - One by TestUser3 for story 1
    - One bookmark by TestUser1 for story 5    
    - Branch content is generated from markov chain generator (markov.py) 
      using clever-grethel.txt, rabbits-bride.txt, and six-soldiers-of-fortune.txt
      as input

### References

The excerpts clever-grethel.txt, rabbits-bride.txt, and six-soldiers-of-fortune.txt are from 
    [The Project Gutenberg](https://www.gutenberg.org/) [EBook of Household Stories by the Brothers Grimm](https://www.gutenberg.org/ebooks/19068), by Jacob Grimm and Wilhelm Grimm

