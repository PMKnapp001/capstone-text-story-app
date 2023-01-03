from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    if not session.get('user_id'):

        return redirect('/users')
    else:    
        return render_template('homepage.html')


@app.route('/search')
def search_page():
    
    return render_template('search.html')

# @app.route('/search', methods=["POST"])
# def submit_search():

#     user_or_story = request.form.get('search-for')
#     search_text = request.form.get('search-text')

#     results = crud.search_user_or_story(user_or_story, search_text)

#     return redirect('/search')

@app.route('/users')
def users():
    
    session['user_id'] = ""

    return render_template("account.html")


@app.route('/users/new', methods=["POST"])
def new_user():

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

    user = crud.get_user_by_id(user_id)

    return render_template('userprofile.html', user=user)


@app.route('/user/logout')
def user_logout():

    session['user_id'] = ""

    return redirect('/')


@app.route('/user/<user_id>/stories')
def all_stories(user_id):

    session['story_id'] = []
    session['intro_branch_id'] = []
    session['previous_branch_id'] = []
    user = crud.get_user_by_id(user_id)
    stories = user.stories

    return render_template('showstories.html', user=user, stories=stories)


@app.route('/user/<user_id>/stories/<story_id>')
def view_story(user_id, story_id):
     
    user = crud.get_user_by_id(user_id)

    story = crud.get_story_by_id(story_id)
    session['story_id'] = story_id

    intro_id = story.first_branch_id
    session['intro_branch_id'] = intro_id
    if intro_id:
        intro = crud.get_branch_by_id(intro_id)
        
    else:
        intro = ""

    all_branches = story.branches

    favorite = crud.get_favorite(user_id = session['user_id'], story_id = story_id)

    rating = crud.get_rating(user_id = session['user_id'], story_id = story_id)

    return render_template('playstory.html', user=user,story=story,intro=intro,all_branches=all_branches, favorite=favorite, rating=rating)


@app.route('/api/branch')
def get_branch():
    clicked_branch_id = int(request.args.get('branch_id'))

    branch = crud.get_branch_by_id(clicked_branch_id)

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

    favorite = crud.create_favorite(user_id = session['user_id'], story_id = story_id)

    db.session.add(favorite)
    db.session.commit()

    story = crud.get_story_by_id(story_id)
    
    flash(f"{story.title} successfully added to favorites.")

    return redirect(f'/user/{story.user_id}/stories/{story_id}')


@app.route('/favorites/<story_id>/remove')
def remove_favorite(story_id):

    crud.delete_favorite(user_id = session['user_id'], story_id = story_id)
    
    story = crud.get_story_by_id(story_id)

    flash(f"{story.title} successfully removed from favorites.")

    return redirect(f'/user/{story.user_id}/stories/{story_id}')



@app.route('/stories/new')
def new_story():

    session['story_id'] = ""
    session['intro_branch_id'] = ""
    session['previous_branch_id'] = ""

    return render_template('createstory.html')


@app.route('/stories/<story_id>/ratings/new', methods=["POST"])
def add_rating(story_id):

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

    title = request.form.get('title')
    synopsis = request.form.get('synopsis')
    user_id = session['user_id']
    new_story = crud.create_story(user_id=user_id, synopsis=synopsis, title=title)

    db.session.add(new_story)
    db.session.commit()

    story_id = new_story.story_id

    print(f"story_id = {story_id}")

    session['story_id'] = story_id
  
    flash(f"Story created.")

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/branches/<branch_id>/updateid')
def update_prev_branch_id(story_id, branch_id):
    
    story_id = story_id

    session['previous_branch_id'] = branch_id

    return redirect(f'/stories/{story_id}/branches/new')


@app.route('/stories/<story_id>/branches/new')
def new_branch(story_id):

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

    crud.delete_story(story_id)

    return redirect(f"/user/{session['user_id']}/stories")


@app.route('/stories/<story_id>/delete/branches/<branch_id>')
def delete_branch(story_id, branch_id):

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

    story = crud.get_story_by_id(story_id)
    story.title = request.form.get('title')
    story.synopsis = request.form.get('synopsis')

    db.session.add(story)
    db.session.commit()

    return redirect(f'/stories/{story_id}/edit')


@app.route('/stories/<story_id>/edit/branches/<branch_id>')
def get_branch_to_edit(story_id, branch_id):

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

    story = crud.get_story_by_id(story_id)

    branches = story.branches
    story_tree = story.make_story_tree()

    return render_template('showbranches.html', story=story, story_tree=story_tree, branches=branches)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



# *commit and push before branches*
# git branch branch-name
# git checkout branchname
# *git checkout main to return to original branch*

# /stories/<story_id>  - GET, displays representation of story

# /stories/new - GET display form to create story
# /stories/new - POST saves form to db (intro-branch-id IS NULL), redirect to /stories/<story_id>/branches/new

# /stories/<story_id>/intro_branch/new - GET display form to create a branch
#     return render_template("intro_branch.html", story=story)
# /stories/<story_id>/intro_branch/new - POST save data from that form, redirect to /stories/<story_id>/braches/<intro_branch_id>/branches/new

# /stories/<story_id>/braches/<branch_id>/branches/new - GET display a form to add subbranch to <branch_id>


# return redirect(f'/stories/{story_id}/branches/new')