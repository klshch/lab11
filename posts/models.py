from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.TIMESTAMP, default=datetime.now)
    type = db.Column(db.Enum('news', 'publication', 'other'), default='other')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post {self.id}: {self.title}."
