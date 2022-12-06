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
ordinal = 0

test_intro_branch = crud.create_branch(story_id=test_story.story_id, 
                                    prev_branch_id = None, 
                                    description=test_intro_desc, 
                                    body=test_intro_body,
                                    branch_prompt=test_branch_prompt,
                                    is_end=is_end,
                                    ordinal=ordinal)

model.db.session.add(test_intro_branch)
model.db.session.commit()

test_story.first_branch_id = test_intro_branch.branch_id

model.db.session.add(test_story)
model.db.session.commit()
