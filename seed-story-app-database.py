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


def create_branches(story, prev_branch, path_level, markov_text):
    """Creates and adds two branches to story in databse."""

    # test branch records for test story
    for i in range(2):
        test_body = markov.make_new_story(markov_text)
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
test_story1 = crud.create_story(test_user.user_id, test_synopsis, test_title)
model.db.session.add(test_story1)
model.db.session.commit()

test_synopsis = "This is the synopsis for the second test story."
test_title = "The Test II: The Retake"
test_story2 = crud.create_story(test_user.user_id, test_synopsis, test_title)
model.db.session.add(test_story2)
model.db.session.commit()

test_synopsis = "This is the synopsis for the third test story."
test_title = "TT3: Pass/Fail"
test_story3 = crud.create_story(test_user.user_id, test_synopsis, test_title)
model.db.session.add(test_story3)
model.db.session.commit()



# test intro branch record for test story
new_soldiers = markov.make_new_story("six-soldiers-of-fortune.txt")

test_intro_body1 = new_soldiers
test_intro_desc1 = "Intro Branch"
test_branch_prompt1 = "Choose the next branch: "
is_end1 = False
ordinal1 = crud.get_ordinal_for_next_branch()

test_intro_branch1 = crud.create_branch(story_id=test_story1.story_id, 
                                    prev_branch_id = None, 
                                    description=test_intro_desc1, 
                                    body=test_intro_body1,
                                    branch_prompt=test_branch_prompt1,
                                    is_end=is_end1,
                                    ordinal=ordinal1)

model.db.session.add(test_intro_branch1)
model.db.session.commit()



new_grethel = markov.make_new_story("clever-grethel.txt")

test_intro_body2 = new_grethel
test_intro_desc2 = "Intro Branch2"
test_branch_prompt2 = "(2)Choose the next branch: "
is_end2 = False
ordinal2 = crud.get_ordinal_for_next_branch()

test_intro_branch2 = crud.create_branch(story_id=test_story2.story_id, 
                                    prev_branch_id = None, 
                                    description=test_intro_desc2, 
                                    body=test_intro_body2,
                                    branch_prompt=test_branch_prompt2,
                                    is_end=is_end2,
                                    ordinal=ordinal2)

model.db.session.add(test_intro_branch2)
model.db.session.commit()



new_rabbit = markov.make_new_story("rabbits-bride.txt")

test_intro_body3 = new_rabbit
test_intro_desc3 = "Intro Branch3"
test_branch_prompt3 = "(3)Choose the next branch: "
is_end3 = False
ordinal3 = crud.get_ordinal_for_next_branch()

test_intro_branch3 = crud.create_branch(story_id=test_story3.story_id, 
                                    prev_branch_id = None, 
                                    description=test_intro_desc3, 
                                    body=test_intro_body3,
                                    branch_prompt=test_branch_prompt3,
                                    is_end=is_end3,
                                    ordinal=ordinal3)

model.db.session.add(test_intro_branch3)
model.db.session.commit()


#Updating first_branch_id in test_story
test_story1.first_branch_id = test_intro_branch1.branch_id

model.db.session.add(test_story1)
model.db.session.commit()

create_branches(test_story1, test_intro_branch1, "a", "six-soldiers-of-fortune.txt")

a_branches = model.Branch.query.filter(model.Branch.prev_branch_id == test_intro_branch1.branch_id).order_by(model.Branch.ordinal).all()

for branch in a_branches:
    create_branches(test_story1, branch, "b", "six-soldiers-of-fortune.txt")



test_story2.first_branch_id = test_intro_branch2.branch_id

model.db.session.add(test_story2)
model.db.session.commit()

create_branches(test_story2, test_intro_branch2, "a", "clever-grethel.txt")

a_branches = model.Branch.query.filter(model.Branch.prev_branch_id == test_intro_branch2.branch_id).order_by(model.Branch.ordinal).all()

for branch in a_branches:
    create_branches(test_story2, branch, "b", "clever-grethel.txt")



test_story3.first_branch_id = test_intro_branch3.branch_id

model.db.session.add(test_story3)
model.db.session.commit()

create_branches(test_story3, test_intro_branch3, "a", "rabbits-bride.txt")

a_branches = model.Branch.query.filter(model.Branch.prev_branch_id == test_intro_branch3.branch_id).order_by(model.Branch.ordinal).all()

for branch in a_branches:
    create_branches(test_story3, branch, "b", "rabbits-bride.txt")


test_story_tree = test_story1.make_story_tree()

# print(test_story_tree)


