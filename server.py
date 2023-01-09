from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Route to homepage for web app. Redirects to
    login if no user_id in session."""

    if not session.get('user_id'):
        return redirect('/users')

    else:    
        return render_template('homepage.html')


@app.route('/search')
def search_page():
    """Route for search page."""

    return render_template('search.html')


@app.route('/users')
def users():
    """Route for user login page. Can only be accessed 
    if no user_id in session. Wipes session when redirected 
    by logout."""

    session['user_id'] = ""
    session['story_id'] = []
    session['intro_branch_id'] = []
    session['previous_branch_id'] = []

    return render_template("account.html")


@app.route('/users/new', methods=["POST"])
def new_user():
    """User account creation route. Checks db if user information
    already present. Flashes respective message if found. Adds user 
    record to db otherwise."""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_username(username):
        flash(f"Account with username {username} already created.")
        return redirect("/users")

    elif crud.get_user_by_email(email):
        flash(f"Account with email {email} already created.")
        return redirect("/users")    

    else:
        user = crud.create_user(username=username,email=email,password=password)

        db.session.add(user)
        db.session.commit()

        flash(f"User {username} created.")

        return redirect('/')


@app.route('/users/login', methods=["POST"])
def login_user():
    """User login route. Checks for credentials and password
    authentication. Flashes respective message if invalid data
    posted. Logs in and adds user_id to session otherwise."""

    username = request.form.get('username')
    password = request.form.get('password')

    user_from_db = crud.get_user_by_username(username)

    if user_from_db:
        if password == user_from_db.password:
            user_id = user_from_db.user_id

            session['user_id'] = user_id

            flash(f"Logged in as {username}.")

            return redirect('/')

        else:
            flash("Password Incorrect.")

            return redirect("/users") 

    else:
        flash(f"No account with username {username} exists.")

        return redirect("/users")


@app.route('/users/<user_id>/profile')
def show_profile(user_id):
    """User profile route."""

    user = crud.get_user_by_id(user_id)

    return render_template('userprofile.html', user=user)


@app.route('/user/logout')
def user_logout():
    """Logout route, clears user_id from session and redirects."""

    session['user_id'] = ""

    return redirect('/')


@app.route('/user/<user_id>/stories')
def all_stories(user_id):
    """User stories route. Page shows all stories for user."""

    session['story_id'] = []
    session['intro_branch_id'] = []
    session['previous_branch_id'] = []
    user = crud.get_user_by_id(user_id)
    stories = user.stories

    return render_template('showstories.html', user=user, stories=stories)


@app.route('/user/<user_id>/stories/<story_id>')
def view_story(user_id, story_id):
    """Story view route. Displays story info for user to play through."""

    user = crud.get_user_by_id(user_id)
    story = crud.get_story_by_id(story_id)
    intro_id = story.first_branch_id
    session['story_id'] = story_id
    session['intro_branch_id'] = intro_id
    
    if intro_id:
        intro = crud.get_branch_by_id(intro_id)
        
    else:
        intro = ""

    all_branches = story.branches
    favorite = crud.get_favorite(user_id = session['user_id'], story_id = story_id)
    rating = crud.get_rating(user_id = session['user_id'], story_id = story_id)
    bookmark = crud.get_bookmark_for_story(session['user_id'], story_id)
    
    if bookmark:
        bookmarked_story = bookmark.story_so_far()
    else:
        bookmarked_story = None

    return render_template('playstory.html', 
                            user=user,story=story, 
                            bookmark=bookmark,
                            intro=intro,all_branches=all_branches, 
                            favorite=favorite, 
                            rating=rating, 
                            bookmarked_story=bookmarked_story)


@app.route('/user/<user_id>/stories/<story_id>/bookmark/delete')
def delete_bookmark(user_id, story_id):
    """Deletes bookmark and restarts story."""

    crud.delete_bookmark(user_id, story_id)
    story = crud.get_story_by_id(story_id)
    user_id = story.user_id

    return redirect(f'/user/{user_id}/stories/{story_id}')


@app.route('/api/branch')
def get_branch():
    """AJAX promise route. Returns branch info for story update."""

    clicked_branch_id = int(request.args.get('branch_id'))
    branch = crud.get_branch_by_id(clicked_branch_id)

    if session['user_id'] != branch.story.user_id:
        if not branch.get_next_branches():
            is_fin = True

        else:
            is_fin = False

        bookmark = crud.get_bookmark_for_story(session['user_id'], branch.story_id)

        if bookmark:
            bookmark.branch_id = clicked_branch_id
            bookmark.is_fin = is_fin
            
        else:
            bookmark = crud.create_bookmark(session['user_id'], branch.story_id, clicked_branch_id, is_fin)

        db.session.add(bookmark)
        db.session.commit()

    if branch.get_next_branches():
        branch_prompt = branch.branch_prompt

    else:
        branch_prompt = "Fin."

    branch_json = jsonify({'branch_id':branch.branch_id,
                    'body':branch.body,
                    'branch_prompt':branch_prompt
                    })
    
    return branch_json


@app.route('/api/search')
def get_results():
    """AJAX promise route. Returns stories or users that contain submitted 
    characters or words in username or title. Updates search page."""

    user_or_story = request.args.get('user_or_story')
    search_text = request.args.get('search_text')

    if len(search_text) < 1:
        results_json = {}

        return results_json

    results = crud.search_user_or_story(user_or_story, search_text)
    results_dict = {}

    if user_or_story == 'user':
        for i in range(len(results)):
            results_dict[i] = {'username': results[i].username,
                               'user_id': results[i].user_id}

    else:
        for i in range(len(results)):
            results_dict[i] = {'title': results[i].title,
                               'story_id': results[i].story_id,
                               'user_id': results[i].user_id}

    results_json = jsonify(results_dict)
    
    return results_json


@app.route('/favorites/<story_id>/add')
def add_favorite(story_id):
    """Creates favorite for story."""

    favorite = crud.create_favorite(user_id = session['user_id'], story_id = story_id)
    db.session.add(favorite)
    db.session.commit()
    story = crud.get_story_by_id(story_id) 
    flash(f"{story.title} successfully added to favorites.")

    return redirect(f'/user/{story.user_id}/stories/{story_id}')


@app.route('/favorites/<story_id>/remove')
def remove_favorite(story_id):
    """Deletes favorite for story."""

    crud.delete_favorite(user_id = session['user_id'], story_id = story_id) 
    story = crud.get_story_by_id(story_id)
    flash(f"{story.title} successfully removed from favorites.")

    return redirect(f'/user/{story.user_id}/stories/{story_id}')


@app.route('/stories/popular')
def get_popular_stories():
    """Displays top ten popular stories with the amount of
    ratings and average rating. Ordered by number of ratings."""

    top_ten_popular = crud.get_top_ten_popular_stories()
    stories = []

    for story_id, number_of_ratings in top_ten_popular:
        story = crud.get_story_by_id(story_id)
        avg_rating = story.get_average_rating()
        stories.append([story, number_of_ratings, avg_rating])
    
    return render_template('popular.html', stories=stories)
    


@app.route('/stories/new')
def new_story():
    """Story creation route. Clears session of story and branch references."""

    session['story_id'] = ""
    session['intro_branch_id'] = ""
    session['previous_branch_id'] = ""

    return render_template('createstory.html')


@app.route('/stories/<story_id>/ratings/new', methods=["POST"])
def add_rating(story_id):
    """Ratings route, submits new rating for story or edits current 
    one if rating exists. Every user can have one rating for every story 
    (not inluding theirs)."""

    user_id = session['user_id']
    rating = crud.get_rating(user_id = session['user_id'], story_id = story_id)
    story = crud.get_story_by_id(story_id)
    score = request.form.get('rating')

    if rating:
        rating.score = score

    else:
        rating = crud.create_rating(score=score, user_id=user_id, story_id=story.story_id)

    db.session.add(rating)
    db.session.commit()
    flash(f"Rating for {story.title} successfully submitted.")

    return redirect(f'/user/{user_id}/stories/{story.story_id}')


@app.route('/stories/new', methods=["POST"])
def add_story():
    """Submits new story to db."""

    title = request.form.get('title')
    synopsis = request.form.get('synopsis')
    user_id = session['user_id']
    new_story = crud.create_story(user_id=user_id, synopsis=synopsis, title=title)
    db.session.add(new_story)
    db.session.commit()
    story_id = new_story.story_id
    session['story_id'] = story_id

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/branches/<branch_id>/updateid') # TODO: Update to redirect to story edit.
def update_prev_branch_id(story_id, branch_id):
    """Updates previous branch id in session. Updated previous branch id
    used with create story template for story traversal."""

    story_id = story_id
    session['previous_branch_id'] = branch_id

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/branches/new')
def new_branch(story_id):
    """Createstory route, gets branch info of previous branches 
    (if not creating intro branch)."""

    story = crud.get_story_by_id(story_id)

    if session['previous_branch_id']:
        prev_branch = crud.get_branch_by_id(session['previous_branch_id'])
        ancestor = crud.get_branch_by_id(prev_branch.prev_branch_id)
        siblings = prev_branch.get_next_branches()

    else:
        siblings = []
        ancestor = []

    return render_template('createstory.html', story=story, siblings=siblings, ancestor=ancestor)



@app.route('/stories/<story_id>/branches/new', methods=["POST"])
def add_branch(story_id):
    """Add branch route, gets info for branch from form and submits 
    to db. Redirects to fresh form with updated references for traversal."""

    story = crud.get_story_by_id(story_id)

    if not session['intro_branch_id']:
        prev_branch_id = None
        story_id = story.story_id
        description = "Intro Branch, no description"
        body = request.form.get('body')
        branch_prompt = request.form.get('prompt')
        ordinal = 0

        branch = crud.create_branch(story_id=story_id, 
                                        prev_branch_id = prev_branch_id, 
                                        description = description, 
                                        body = body,
                                        branch_prompt = branch_prompt,
                                        ordinal=ordinal)

        db.session.add(branch)
        db.session.commit()

        story_to_update = crud.get_story_by_id(story_id)    
        branch_id = branch.branch_id
        story_to_update.first_branch_id = branch_id

        db.session.add(story_to_update)
        db.session.commit() 

        session['intro_branch_id'] = branch_id
        session['previous_branch_id'] = branch_id

    else:
        prev_branch_id = session['previous_branch_id']
        story_id = story.story_id
        description = request.form.get('description')
        body = request.form.get('body')
        branch_prompt = request.form.get('prompt')
        next= request.form.get('next')
        ordinal = crud.get_ordinal_for_next_branch(prev_branch_id)

        branch = crud.create_branch(story_id=story_id, 
                                        prev_branch_id = prev_branch_id, 
                                        description = description, 
                                        body = body,
                                        branch_prompt = branch_prompt,
                                        ordinal=ordinal)

        db.session.add(branch)
        db.session.commit()
        
        branch_id = branch.branch_id

        if next == "child":
            session['previous_branch_id'] = branch_id
      
    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/edit')
def get_story_to_edit(story_id):
    """Edit story route, gets story and intro branch data
    (if intro branch created) and begins edit story form from
    beginning of story."""

    story = crud.get_story_by_id(story_id)
    session['story_id'] = story_id

    if story.first_branch_id:
        session['intro_branch_id'] = story.first_branch_id

    else:
        session['intro_branch_id'] = ""

    session['previous_branch_id'] = ""
    story = crud.get_story_by_id(story_id)

    return render_template(f'editstory.html', story=story)


@app.route('/stories/<story_id>/delete')
def delete_story(story_id):
    """Route deletes story."""

    crud.delete_story(story_id)

    return redirect(f"/user/{session['user_id']}/stories")


@app.route('/stories/<story_id>/delete/branches/<branch_id>')
def delete_branch(story_id, branch_id):
    """Deletes branch and updates session data for story 
    traversal while editing. Redirects to creation route
    if intro branch deleted."""

    branch = crud.get_branch_by_id(branch_id)
    prev_branch_id = branch.prev_branch_id
    crud.delete_branch_and_descendants(branch_id)

    if prev_branch_id:
        branch_id = prev_branch_id

        return redirect(f'/stories/{story_id}/edit/branches/{branch_id}')
    
    session['previous_branch_id'] = ""
    session['intro_branch_id'] = ""

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/edit', methods=["POST"])
def edit_story(story_id):
    """Updates story data in db after edit."""

    story = crud.get_story_by_id(story_id)
    story.title = request.form.get('title')
    story.synopsis = request.form.get('synopsis')
    db.session.add(story)
    db.session.commit()

    return redirect(f'/stories/{story_id}/edit')


@app.route('/stories/<story_id>/edit/branches/<branch_id>')
def get_branch_to_edit(story_id, branch_id):
    """Get branch data from db to edit. Updates session
    info for edit story traversal."""

    story = crud.get_story_by_id(story_id)
    branch = crud.get_branch_by_id(branch_id)
    session['intro_branch_id'] = story.first_branch_id

    if session['intro_branch_id']:
        children = branch.get_next_branches()
        siblings = []
        ancestor = []
        
        if story.first_branch_id != branch.branch_id:
            session['previous_branch_id'] = branch.prev_branch_id
            prev_branch = crud.get_branch_by_id(session['previous_branch_id'])
            ancestor = crud.get_branch_by_id(prev_branch.prev_branch_id)
            siblings = prev_branch.get_next_branches()
            siblings.pop(siblings.index(branch))
        
        return render_template('editbranch.html', story=story, branch=branch, siblings=siblings, ancestor=ancestor, children=children)

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/edit/branches/<branch_id>', methods=["POST"])
def edit_branch(story_id, branch_id):
    """Updates branch in db after edit."""

    story = crud.get_story_by_id(story_id)
    branch = crud.get_branch_by_id(branch_id)

    if story.first_branch_id != branch.branch_id:
        branch.description = request.form.get('description')

    branch.body = request.form.get('body')
    branch.branch_prompt = request.form.get('prompt')
    db.session.add(branch)
    db.session.commit()

    return redirect(f'/stories/{story_id}/edit/branches/{branch_id}')


@app.route('/stories/<story_id>/branches')
def show_branches(story_id):
    """Shows complete story tree with links for each branch."""

    story = crud.get_story_by_id(story_id)
    branches = story.branches
    story_tree = story.make_story_tree()

    return render_template('showbranches.html', story=story, story_tree=story_tree, branches=branches)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)