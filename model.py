"""Models for Interactive Text Story App"""

from flask_sqlalchemy import SQLAlchemy

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
    first_branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable = False)

    # Relationships for primary keys and foreign keys
    user = db.relationship("User", back_populates="stories")
    first_branch = db.relationship("Branch", back_populates="story_intro")
    branches = db.relationship("Branch", back_populates="story")
    ratings = db.relationship("Rating", back_populates="story")
    
    
    def __repr__(self):
        """Displays info from story class."""
        
        return f"<Story story_id={self.story_id} title={self.title}>"


class Branch(db.Model):
    """Branch class."""
    
    __tablename__ = "branches"

    # SQLAlchemy instructions to create table
    branch_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'), nullable = False)
    prev_branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable = False, default = 0)
    description = db.Column(db.Text, nullable = False)
    body = db.Column(db.Text, nullable = False)
    branch_prompt = db.Column(db.Text)
    is_end = db.Column(db.Boolean, nullable = False, default = False)
    ordinal = db.Column(db.Integer, nullable = False, default = 0)

    # Relationships for primary keys and foreign keys
    story = db.relationship("Story", back_populates="branches")
    prev_branch = db.relationship("Branch", back_populates="branch_options")
    branch_options = db.relationship("Branch", back_populates="prev_branch")
    story_intro = db.relationship("Story", back_populates="first_branch")


    def __repr__(self):
        """Displays info from branch class."""
        
        return f"<Branch branch_id={self.branch_id} prev_branch_id={self.prev_branch_id} story_id={self.story_id}>"


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