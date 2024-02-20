"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://yt3.ggpht.com/-_fExgATRXLY/AAAAAAAAAAI/AAAAAAAAAAA/-fmo8LhN7Pg/s240-c-k-no-rj-c0xffffff/photo.jpg'

class User(db.Model):
    """User class"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Get full name"""
        return f'{self.first_name} {self.last_name}'

def connect_db(app):
    """Connect db to flask app"""
    db.app = app
    db.init_app(app)

