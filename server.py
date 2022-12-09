from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/test-play-story')
def test_story():

    story = crud.get_story_by_id(1)

    intro = story.get_intro_branch()

    # all_branches = crud.get_all_branches_from_story_id(story.story_id)

    all_branches = story.branches

    # branches = intro.get_next_branches()

    # end = False

    return render_template('test.html', story=story, intro=intro, all_branches=all_branches)


@app.route('/api/branch')
def get_branch():
    next_branch_id = int(request.args.get('branch_id'))

    branch = crud.get_branch_by_id(next_branch_id)
    # next_branches = branch.get_next_branches()
    # branches = []
    # for branch in next_branches:
    #     branches.append(branch.branch_id)

    branch_json = jsonify({'branch_id':branch.branch_id,
                    'body':branch.body,
                    'branch_prompt':branch.branch_prompt,
                    'is_end':branch.is_end
                    })
    
    return branch_json


# @app.route('/api/next-branch')
# def get_branch():
#     next_branch_id = int(request.args.get('branch_id'))

#     branch = crud.get_branch_by_id(next_branch_id)
#     branches = branch.get_next_branches()

#     branches_json = jsonify({'branch_id':branch.branch_id,
#                     'body':branch.body,
#                     'branch_prompt':branch.branch_prompt,
#                     'is_end':branch.is_end
#                     })
    
#     return branch_json


@app.route('/test-create-story')
def create_story():

    session['story_id'] = []
    session['intro_branch_id'] = []

    return render_template('createstory.html')



@app.route('/add-story', methods=["POST"])
def add_story():

    title = request.form.get('title')
    synopsis = request.form.get('synopsis')
    user_id = 1 # set to 1 for testing, use form.get when implemented

    new_story = crud.create_story(user_id=user_id, synopsis=synopsis, title=title)

    db.session.add(new_story)
    db.session.commit()

    new_story_id = new_story.story_id

    session['story_id'] = new_story_id
    session['title'] = title
    session['synopsis'] = synopsis

    flash(f"Story created.")

    return render_template('createstory.html')



@app.route('/add-intro', methods=["POST"])
def add_intro():

    prev_branch = None
    story_id = session['story_id']
    description = "Intro Branch, no description"
    body = request.form.get('body')
    branch_prompt = request.form.get('prompt')
    is_end = request.form.get('is-end')
    ordinal = 0

    if is_end == "true":
        is_end = True
    else:
        is_end = False

    intro_branch = crud.create_branch(story_id=story_id, 
                                    prev_branch_id = prev_branch, 
                                    description = description, 
                                    body = body,
                                    branch_prompt = branch_prompt,
                                    is_end=is_end,
                                    ordinal=ordinal)

    db.session.add(intro_branch)
    db.session.commit()    

    intro_branch_id = intro_branch.branch_id

    story_to_update = crud.get_story_by_id(session['story_id'])

    story_to_update.first_branch_id = intro_branch_id

    db.session.add(story_to_update)
    db.session.commit()   

    session['intro_branch_id'] = intro_branch_id
    session['previous_branch_id'] = intro_branch_id



    # print(f"intro branch id = {session['intro_branch_id']}")
    # print(f"prev branch id = {session['previous_branch_id']}")
    # print(f"story id{session['story_id']}")


    return render_template('createbranches.html', story=story_to_update, intro=intro_branch)

# @app.route('/api/get-previous-branch')
# def get_previous_branch():
    
#     print(f"in route from session prev branch id = ")

#     # branch_id = session['previous_branch_id']

#     # print(f"in route from session variable = {branch_id}")

#     # branch = crud.get_branch_by_id(branch_id)

#     return jsonify()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)