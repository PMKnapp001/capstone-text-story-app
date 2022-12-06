"""Create, Read, Update, Delete Operations for Capstone Text Story App"""

from model import db, User, Story, Branch, Rating, connect_to_db


def create_user(username, password, email):
    """Creates a user."""

    user = User(username=username, password=password, email=email)

    return user


def create_story(user_id, synopsis, title):
    """Creates a story."""

    story = Story(user_id=user_id, synopsis=synopsis, title=title)

    return story


def create_branch(story_id, prev_branch_id, description, body, branch_prompt, is_end, ordinal):
    """Creates a branch."""

    branch = Branch(story_id=story_id, 
                    prev_branch_id=prev_branch_id,
                    description=description,
                    body=body,
                    branch_prompt=branch_prompt,
                    is_end=is_end,
                    ordinal=ordinal)

    return branch


def create_rating(score, user_id, story_id):
    """Creates a rating."""
    
    rating = Rating(score=score, user_id=user_id, story_id=story_id)

    return rating


def get_all_stories():
    """"Gets story_id and title of all stories as list."""
    
    all_stories = db.session.query(Story.story_id, Story.title).all()

    return all_stories


def get_story_by_id(story_id):
    """"Gets a story by id"""

    story = Story.query.get(story_id)

    if story:
        return story
    
    else:
        return None


def get_all_users():
    """"Gets all users as list."""

    return User.query.all()


def get_user_by_id(user_id):
    """"Gets a user by id"""

    user = User.query.get(user_id)

    if user:
        return user
    
    else:
        return None


def get_user_by_username(username):
    """Gets a user by username"""

    user = User.query.filter(User.username == username).first()

    if user:
        return user
    
    else:
        return None


def get_user_by_email(email):
    """Gets a user by email"""

    user = User.query.filter(User.email== email).first()

    if user:
        return user
    
    else:
        return None


def get_ratings_by_user(user_id):
    """Gets all ratings by user as list."""

    ratings = Rating.query.filter(Rating.user_id == user_id).all()

    if ratings:
        return ratings
    
    else:
        return None


def get_ratings_for_story(story_id):
    """Gets all ratings for a story as list."""

    ratings = Rating.query.filter(Rating.story_id == story_id).all()

    if ratings:
        return ratings
    
    else:
        return None    





if __name__ == '__main__':
    from server import app
    connect_to_db(app)