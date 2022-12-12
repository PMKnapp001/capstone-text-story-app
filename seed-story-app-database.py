"""Instructions to create and populated database for capstone story app."""

import os
import json
from random import choice, randint

import crud
import model
import server
import markov

os.system("dropdb text-story-app")
os.system("createdb text-story-app")
model.connect_to_db(server.app)
model.db.create_all()


def create_branches(story, prev_branch, path_level):
    """Creates and adds two branches to story in databse."""

    # test branch records for test story
    for i in range(2):
        test_body = markov.make_new_story("six-soldiers-of-fortune.txt")
        test_desc = f"Path {path_level}-{i}"
        test_branch_prompt = f"({path_level}-{i})Choose the next branch: "
        is_end = False
        ordinal = crud.get_ordinal_for_next_branch(prev_branch.branch_id)

        test_branch = crud.create_branch(story_id=story.story_id, 
                                            prev_branch_id = prev_branch.branch_id, 
                                            description=test_desc, 
                                            body=test_body,
                                            branch_prompt=test_branch_prompt,
                                            is_end=is_end,
                                            ordinal=ordinal)

        model.db.session.add(test_branch)
        model.db.session.commit()

# test user record
test_user = crud.create_user(username="TestUser", password="TestPass", email="user@email.test")

model.db.session.add(test_user)
model.db.session.commit()


# test story record
test_synopsis = "This is the synopsis for a test story."
test_title = "The Test"

test_story = crud.create_story(test_user.user_id, test_synopsis, test_title)

model.db.session.add(test_story)
model.db.session.commit()


# test intro branch record for test story
new_soldiers = markov.make_new_story("six-soldiers-of-fortune.txt")

test_intro_body = new_soldiers
test_intro_desc = "Intro Branch"
test_branch_prompt = "Choose the next branch: "
is_end = False
ordinal = crud.get_ordinal_for_next_branch()

test_intro_branch = crud.create_branch(story_id=test_story.story_id, 
                                    prev_branch_id = None, 
                                    description=test_intro_desc, 
                                    body=test_intro_body,
                                    branch_prompt=test_branch_prompt,
                                    is_end=is_end,
                                    ordinal=ordinal)

model.db.session.add(test_intro_branch)
model.db.session.commit()


#Updating first_branch_id in test_story
test_story.first_branch_id = test_intro_branch.branch_id

model.db.session.add(test_story)
model.db.session.commit()

create_branches(test_story, test_intro_branch, "a")

a_branches = model.Branch.query.filter(model.Branch.prev_branch_id == test_intro_branch.branch_id).order_by(model.Branch.ordinal).all()

for branch in a_branches:
    create_branches(test_story, branch, "b")




