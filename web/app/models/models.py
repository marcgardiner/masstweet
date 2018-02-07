#/app/models/models.py

from app import db


class User(db.Model):
    """Model User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)


    def __init__(self, email, password):
        """initial model instance"""

        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    
    def password_is_valid(self, password):
        """check if password is valid"""

        return Bcrypt().check_password_hash(self.password, password)


    def save(self):
        """save instance"""

        db.session.add(self)
        db.session.commit()
