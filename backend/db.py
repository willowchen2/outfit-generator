from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Piece(db.Model):
    __tablename__="wardrobe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.Integer, nullable=False) #nulllable=false means that this every item needs to have a  label
    color = db.Column(db.String, nullable=False)
    image=db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.label=kwargs.get("label", "")
        self.image=kwargs.get("image", "")
        self.color=kwargs.get("color", "")

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "color": self.color,
            "image": self.image
        }




