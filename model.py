"""Models for Interactive Text Story App"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()


class User(db.Model):
    """User class."""
    
    __tablename__ = "users"

    # SQLAlchemy instructions to create table
    user_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    username = db.Column(db.String, nullable= False, unique=True)
    password = db.Column(db.String, nullable= False)
    email = db.Column(db.String, nullable= False, unique=True)

    # Relationships for primary keys and foreign keys
    stories = db.relationship("Story", back_populates="user")
    ratings = db.relationship("Rating", back_populates="user")
    favorites = db.relationship("Favorite", back_populates="user")
    bookmarks = db.relationship("Bookmark", back_populates="user")


    def __repr__(self):
        """Displays info from user class."""

        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"


class Story(db.Model):
    """Story class."""
    
    __tablename__ = "stories"
    
    # SQLAlchemy instructions to create table
    story_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    synopsis = db.Column(db.Text, nullable = False)
    title = db.Column(db.Text, nullable = False)
    first_branch_id = db.Column(db.Integer)

    # Relationships for primary keys and foreign keys
    user = db.relationship("User", back_populates="stories")
    branches = db.relationship("Branch", back_populates="story")
    ratings = db.relationship("Rating", back_populates="story")
    favorites = db.relationship("Favorite", back_populates="story")
    bookmarks = db.relationship("Bookmark", back_populates="story")
    
    
    # story methods
    def __repr__(self):
        """Displays info from story class."""
        
        return f"<Story story_id={self.story_id} title={self.title}>"


    def get_intro_branch(self):
        """Return branch that serves as intro for story."""

        return Branch.query.filter(Branch.branch_id == self.first_branch_id).first()


    def get_average_rating(self):
            """Returns average rating score for story_id argument."""
 
            all_ratings = Rating.query.filter(Rating.story_id == self.story_id).all()

            if not all_ratings:
                return "No ratings."

            else:
                average_score = 0
                total_score = 0
                count = 0

                for rating in all_ratings:
                    total_score += rating.score
                    count += 1

                average_score = total_score/count
        
                return average_score


    def make_story_tree(self):
        """Returns dictionary of branch ids with current id as key 
        and child branch id as empty dictionarys or or value if that
        branch does not have children."""

        return self.get_intro_branch().make_story_tree()


    def get_branches_by_ordinal(self):

        return Branch.query.filter(Branch.story_id == self.story_id).order_by(Branch.ordinal).all()


class Branch(db.Model):
    """Branch class."""
    
    __tablename__ = "branches"

    # SQLAlchemy instructions to create table
    branch_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'), nullable = False)
    prev_branch_id = db.Column(db.Integer)
    description = db.Column(db.Text, nullable = False)
    body = db.Column(db.Text, nullable = False)
    branch_prompt = db.Column(db.Text)
    ordinal = db.Column(db.Integer, nullable = False, index= True, default = 1)

    # Relationships for primary keys and foreign keys
    story = db.relationship("Story", back_populates="branches")
    bookmarks = db.relationship("Bookmark", back_populates="branch")


    def __repr__(self):
        """Displays info from branch class."""
        
        return f"<Branch branch_id={self.branch_id} prev_branch_id={self.prev_branch_id} story_id={self.story_id}>"


    def get_next_branches(self):
        """Returns all sub branches for current branch."""

        return Branch.query.filter(Branch.prev_branch_id == self.branch_id).order_by(Branch.ordinal).all()


    def make_story_tree(self):
        """Returns dictionary of branch ids with current id as key 
        and child branch id as empty dictionarys or or value if that
        branch does not have children."""

        children_branches=[]
        next_branches = self.get_next_branches()

        for branch in next_branches:
            children_branches.append(branch.make_story_tree())

        branch_tree={"branch_id":self.branch_id, "children":children_branches, "branch_desc":self.description}

        return branch_tree


class Rating(db.Model):
    """Rating class."""
    
    __tablename__ = "ratings"

    # SQLAlchemy instructions to create table
    rating_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'))

    # Relationships for primary keys and foreign keys
    user = db.relationship("User", back_populates="ratings")
    story = db.relationship("Story", back_populates="ratings")


    def __repr__(self):
        """Displays info from rating class."""
        
        return f"<Rating rating_id={self.rating_id} score={self.score} user_id={self.user_id} story_id={self.story_id}>"



class Favorite(db.Model):
    """Favorite class."""

    __tablename__ = "favorites"

    # SQLAlchemy instructions to create table
    favorite_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'))

    # Relationships for primary keys and foreign keys
    user = db.relationship("User", back_populates="favorites")
    story = db.relationship("Story", back_populates="favorites")


    def __repr__(self):
        """Displays info from favorite class."""
        
        return f"<Favorite favorite_id={self.favorite_id} user_id={self.user_id} story_id={self.story_id}>"


    def get_rating_score(self):
        """Returns rating for favorited story by user."""

        rating = Rating.query.filter(Rating.story_id == self.story_id, Rating.user_id == self.user_id).first()

        if not rating:
            score = "No Rating."
        
        else:
            score = rating.score

        return score


class Bookmark(db.Model):
    """Bookmark class."""

    __tablename__ = "bookmarks"

    # SQLAlchemy instructions to create table
    bookmark_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'))
    is_fin = db.Column(db.Boolean, default=False)

    # Relationships for primary keys and foreign keys
    user = db.relationship("User", back_populates="bookmarks")
    story = db.relationship("Story", back_populates="bookmarks")
    branch = db.relationship("Branch", back_populates="bookmarks")


    def __repr__(self):
        """Displays info from bookmark class."""
        
        return f"<Bookmark bookmark_id={self.bookmark_id} user_id={self.user_id} story_id={self.story_id}>"


    def story_so_far(self):
        """Returns list of body texts from previous branches."""

        story_so_far = []
        intro_branch_id = self.story.first_branch_id
        current_branch_id = self.branch_id
        bookmarked_branch = Branch.query.filter(Branch.branch_id == current_branch_id).first()

        if not bookmarked_branch.get_next_branches():
            story_so_far.append("Fin.")

        while current_branch_id != intro_branch_id:
            current_branch = Branch.query.filter(Branch.branch_id == current_branch_id).first()
            story_so_far.append(current_branch.body)
            current_branch_id = current_branch.prev_branch_id

        story_so_far.reverse()

        return story_so_far



def connect_to_db(flask_app, db_uri="postgresql:///text-story-app", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)