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

@app.route('/test')
def test_story():

    story = crud.get_story_by_id(1)

    intro = story.get_intro_branch()

    all_branches = crud.get_all_branches_from_story_id(story.story_id)

    # branches = intro.get_next_branches()

    # end = False

    return render_template('test.html', story=story, intro=intro, all_branches=all_branches)


@app.route('/api/branch')
def get_branch():
    next_branch_id = int(request.args.get('branch_id'))

    branch = crud.get_branch_by_id(next_branch_id)
    next_branches = branch.get_next_branches()
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


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)