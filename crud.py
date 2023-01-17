"""Create, Read, Update, Delete Operations for Capstone Text Story App"""

from model import db, User, Story, Branch, Rating, Favorite, Bookmark, connect_to_db


def create_user(username, password, email):
    """Creates a user."""

    user = User(username=username, password=password, email=email)

    return user


def delete_user(user_id):
    """Deletes ratings, stories, and then user."""

    user = get_user_by_id(user_id)
    all_stories_for_user = Story.query.filter(Story.user_id == user_id).all()
    delete_ratings_for_user(user_id)
    delete_bookmarks_for_user(user_id)
    delete_favorites_for_user(user_id)
    for story in all_stories_for_user:
        delete_story(story.story_id)
    db.session.delete(user)
    db.session.commit()


def create_story(user_id, synopsis, title):
    """Creates a story."""

    story = Story(user_id=user_id, synopsis=synopsis, title=title)

    return story


def delete_story(story_id):
    """Deletes ratings, branches for story and then deletes story."""    

    story = Story.query.get(story_id)
    delete_ratings_for_story(story_id)
    delete_bookmarks_for_story(story_id)
    delete_favorites_for_story(story_id)
    delete_branch_and_descendants(story.first_branch_id)
    db.session.delete(story)
    db.session.commit()


def create_branch(story_id, prev_branch_id, description, body, branch_prompt, ordinal):
    """Creates a branch."""

    branch = Branch(story_id=story_id, 
                    prev_branch_id=prev_branch_id,
                    description=description,
                    body=body,
                    branch_prompt=branch_prompt,
                    ordinal=ordinal)

    return branch


def delete_branch_and_descendants(branch_id):
    """Deletes branch after deleting children branches."""

    if branch_id:
        branch = Branch.query.get(branch_id)
        story = branch.story
        if story.first_branch_id == int(branch_id):
            story.first_branch_id = None
            db.session.add(story)
            db.session.commit()

        for child in branch.get_next_branches():
            delete_bookmarks_for_branch(child.branch_id)
            delete_branch_and_descendants(child.branch_id)
            db.session.delete(child)
            db.session.commit()
        db.session.delete(branch)
        db.session.commit()


def create_rating(score, user_id, story_id):
    """Creates a rating."""
    
    rating = Rating(score=score, user_id=user_id, story_id=story_id)

    return rating


def delete_ratings_for_story(story_id):
    """Deletes ratings for a story."""

    all_ratings_for_story = Rating.query.filter(Rating.story_id == story_id).all()

    for rating in all_ratings_for_story:
        db.session.delete(rating)
        db.session.commit()


def delete_ratings_for_user(user_id):
    """Deletes ratings by a user."""

    all_ratings_for_user = Rating.query.filter(Rating.user_id == user_id).all()

    for rating in all_ratings_for_user:
        db.session.delete(rating)
        db.session.commit()


def get_top_ten_popular_stories():
    """Returns list of top ten popular stories descending."""

    top_ten_popular_stories = db.session.query(
                                                Rating.story_id, db.func.count(Rating.story_id)
                                                ).group_by('story_id').order_by(
                                                db.desc(db.func.count(Rating.story_id))
                                                ).limit(10).all()

    return top_ten_popular_stories


def create_favorite(user_id, story_id):
    """Creates a favorite."""
    
    favorite = Favorite(user_id=user_id, story_id=story_id)

    return favorite


def delete_favorite_with_id(favorite_id):
    """Deletes a favorite."""
    
    favorite_to_delete = Favorite.query.filter(Favorite.favorite_id == favorite_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()


def get_favorite(user_id, story_id):
    """Gets a favorite."""
    
    favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.story_id == story_id).first()

    return favorite


def delete_favorite(user_id, story_id):
    """Deletes a favorite."""
    
    favorite_to_delete = Favorite.query.filter(Favorite.user_id == user_id, Favorite.story_id == story_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()


def delete_favorites_for_user(user_id):
    """Deletes a user's favorites."""

    all_favorites_for_user = Favorite.query.filter(Favorite.user_id == user_id).all()

    for favorite in all_favorites_for_user:
        db.session.delete(favorite)
        db.session.commit()


def delete_favorites_for_story(story_id):
    """Deletes favorites for a story."""

    all_favorites_for_story = Favorite.query.filter(Favorite.story_id == story_id).all()

    for favorite in all_favorites_for_story:
        db.session.delete(favorite)
        db.session.commit()


def create_bookmark(user_id, story_id, branch_id, is_fin):
    """Creates a bookmark for a story."""

    bookmark = Bookmark(user_id=user_id, story_id=story_id, branch_id=branch_id, is_fin=is_fin)

    return bookmark


def delete_bookmark(user_id, story_id):
    """Deletes a bookmark."""
    
    bookmark_to_delete = Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.story_id == story_id).first()

    db.session.delete(bookmark_to_delete)
    db.session.commit()


def delete_bookmarks_for_user(user_id):
    """Deletes a user's bookmarks."""

    all_bookmarks_for_user = Bookmark.query.filter(Bookmark.user_id == user_id).all()

    for bookmark in all_bookmarks_for_user:
        db.session.delete(bookmark)
        db.session.commit()


def delete_bookmarks_for_story(story_id):
    """Deletes bookmarks for a story."""

    all_bookmarks_for_story = Bookmark.query.filter(Bookmark.story_id == story_id).all()

    for bookmark in all_bookmarks_for_story:
        db.session.delete(bookmark)
        db.session.commit()


def delete_bookmarks_for_branch(branch_id):
    """Deletes bookmarks for a branch."""

    all_bookmarks_for_branch = Bookmark.query.filter(Bookmark.branch_id == branch_id).all()

    for bookmark in all_bookmarks_for_branch:
        db.session.delete(bookmark)
        db.session.commit()


def get_bookmark_for_story(user_id, story_id):
    """Gets a user's bookmark for a story."""

    bookmark = Bookmark.query.filter(Bookmark.user_id == user_id, Bookmark.story_id == story_id).first()

    return bookmark


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


def get_branch_by_id(branch_id):
    """"Gets a branch by id"""

    branch = Branch.query.get(branch_id)

    if branch:
        return branch
    
    else:
        return None


def get_all_branches_from_story_id(story_id):
    """Returns all branches for a story."""

    all_branches = Branch.query.filter(Branch.story_id==story_id).all()

    return all_branches


def get_all_branches_for_prompt(prev_branch_id):
    """"Gets sub branches for previous branch."""
    
    all_sub_branches = Branch.query.filter(Branch.prev_branch_id == prev_branch_id).all()

    return all_sub_branches


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


def get_rating(user_id, story_id):
    """Gets a rating using user_id and story_id."""

    rating = Rating.query.filter(Rating.user_id == user_id, Rating.story_id == story_id).first()

    return rating


def get_ordinal_for_next_branch(branch_id = 0):
    """Returns an ordinal value to be used when creating a branch."""
    
    all_sub_branches = Branch.query.filter(Branch.prev_branch_id == branch_id).all()
    ordinal = 1

    for branch in all_sub_branches:
        ordinal +=1

    return ordinal


def search_user_or_story(user_or_story, search_for):
    """Searches for either users or stories that have search_for in username or story title."""

    if user_or_story == 'user':
        results = User.query.filter(User.username.like(f'%{search_for}%')).all() 

    else:
        results = Story.query.filter(Story.title.like(f'%{search_for}%')).all()

    return results



if __name__ == '__main__':
    from server import app
    connect_to_db(app)